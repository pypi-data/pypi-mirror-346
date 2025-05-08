import abc
import warnings

import numpy as np
from streamtracer import StreamTracer, VectorGrid

import astropy.constants as const
import astropy.coordinates as astrocoords
import astropy.units as u

from sunpy.util.decorators import deprecated

import sunkit_magex.pfss
import sunkit_magex.pfss.fieldline as fieldline

__all__ = ['Tracer', 'PerformanceTracer', 'FortranTracer', 'PythonTracer']

class Tracer(abc.ABC):
    """
    Abstract base class for a streamline tracer.
    """
    @abc.abstractmethod
    def trace(self, seeds, output):
        """
        Parameters
        ----------
        seeds : astropy.coordinates.SkyCoord
            Coordinaes of the magnetic field seed points.
        output : sunkit_magex.pfss.Output
            pfss output.

        Returns
        -------
        streamlines : FieldLines
            Traced field lines.
        """

    @staticmethod
    def validate_seeds(seeds):
        """
        Check that *seeds* has the right shape and is the correct type.
        """
        if not isinstance(seeds, astrocoords.SkyCoord):
            raise ValueError(
                f'seeds must be SkyCoord object (got {type(seeds)} instead)'
            )

    @staticmethod
    def cartesian_to_coordinate():
        """
        Convert cartesian coordinate outputted by a tracer to a `~sunkit_magex.pfss.fieldline.FieldLine`
        object.
        """

    @staticmethod
    def coords_to_xyz(seeds, output):
        """
        Given a set of astropy sky coordinates, transoform them to
        cartesian x, y, z coordinates.

        Parameters
        ----------
        seeds : astropy.coordinates.SkyCoord
        output : sunkit_magex.pfss.Output
        """
        seeds = seeds.transform_to(output.coordinate_frame)
        # In general the phi value of the magnetic field array can differ from
        # the longitude value in world coordinates
        lon = seeds.lon
        # Note we want 0deg longitude to be a point on the LH side of the map,
        # but _lon0 is center of map, so offset by 180deg
        lon -= output._lon0 - 180 * u.deg
        x, y, z = astrocoords.spherical_to_cartesian(
            seeds.radius, seeds.lat, lon)
        x = x.to_value(const.R_sun)
        y = y.to_value(const.R_sun)
        z = z.to_value(const.R_sun)
        return x, y, z


class PerformanceTracer(Tracer):
    r"""
    Tracer using compiled code via streamtracer.

    Parameters
    ----------
    max_steps: str, int
        Maximum number of steps each streamline can take before stopping.
        This controls the total amount of memory allocated for all the
        streamlines.

        If ``'auto'`` (the default) this is set to :math:`4n_{r} / ds`, where
        :math:`n_{r}` is the number of radial grid points and :math:`ds` is
        the specified ``step_size``.

    step_size : float
        Step size as a fraction of numerical grid cell size at the equator.
        Must be less than the number of radial coordinate cells.

    Notes
    -----
    Because the stream tracing is done in spherical coordinates, there is a
    singularity at the poles (ie. :math:`s = \pm 1`), which means seeds placed
    directly on the poles will not go anywhere.
    """
    def __init__(self, max_steps='auto', step_size=1):
        self.max_steps = max_steps
        self.step_size = step_size
        self.max_steps = max_steps
        max_steps = 1 if max_steps == 'auto' else max_steps
        self.tracer = StreamTracer(max_steps, step_size)

    @staticmethod
    def vector_grid(output):
        """
        Create a `streamtracer.VectorGrid` object from an `~sunkit_magex.pfss.Output`.
        """
        # The indexing order on the last index is (phi, s, r)
        vectors = output.bg.copy()

        # Correct s direction for coordinate system distortion
        sqrtsg = output.grid._sqrtsg_correction
        # phi correction
        with np.errstate(divide='ignore', invalid='ignore'):
            vectors[..., 0] /= sqrtsg
        # At the poles B_phi is now infinite. Since changes to B_phi at the
        # poles have little effect on the field line, set to zero to allow for
        # easy handline in the streamline integrator
        vectors[:, 0, :, 0] = 0
        vectors[:, -1, :, 0] = 0

        # s correction
        vectors[..., 1] *= -sqrtsg

        grid_spacing = output.grid._grid_spacing
        # Cyclic only in the phi direction
        # (theta direction becomes singular at the poles so it is not cyclic)
        cyclic = [True, False, False]
        origin_coord = [0, -1, 0]
        return VectorGrid(
            vectors, grid_spacing, cyclic=cyclic, origin_coord=origin_coord
        )

    def trace(self, seeds, output):
        if self.max_steps == 'auto':
            self.tracer.max_steps = int(4 * output.grid.nr / self.step_size)

        self.validate_seeds(seeds)
        x, y, z = self.coords_to_xyz(seeds, output)
        r, lat, phi = astrocoords.cartesian_to_spherical(x, y, z)

        # Force 360deg wrapping
        phi = astrocoords.Longitude(phi).to_value(u.rad)
        s = np.sin(lat).to_value(u.dimensionless_unscaled)
        rho = np.log(r)

        seeds = np.atleast_2d(np.stack((phi, s, rho), axis=-1))

        # Get a grid
        vector_grid = self.vector_grid(output)

        # Do the tracing
        #
        # Normalise step size to the radial cell size, so step size is a
        # fraction of the radial cell size.
        self.tracer.ds = self.step_size * output.grid._grid_spacing[2]
        self.tracer.trace(seeds, vector_grid)
        xs = self.tracer.xs

        # Filter out of bounds points out
        rho_ss = np.log(output.grid.rss)
        xs = [x[(x[:, 2] <= rho_ss) & (x[:, 2] >= 0) & (np.abs(x[:, 1]) < 1), :] for x in xs]

        rots = self.tracer.ROT
        if np.any(rots == 1):
            warnings.warn(
                'At least one field line ran out of steps during tracing.\n'
                'You should probably increase max_steps '
                f'(currently set to {self.max_steps}) and try again.')

        xs = [np.stack(sunkit_magex.pfss.coords.strum2cart(x[:, 2], x[:, 1], x[:, 0]), axis=-1) for x in xs]
        flines = [fieldline.FieldLine(x[:, 0], x[:, 1], x[:, 2], output) for x in xs]
        return fieldline.FieldLines(flines)


class PythonTracer(Tracer):
    """
    Tracer using native python code.
    Uses `scipy.integrate.solve_ivp`, with an LSODA method.
    """
    def __init__(self, atol=1e-4, rtol=1e-4):
        """
        dtf : float
            Absolute tolerance of the tracing.
        rtol : float
            Relative tolerance of the tracing.
        """
        self.atol = atol
        self.rtol = rtol

    def trace(self, seeds, output):
        self.validate_seeds(seeds)
        x, y, z = self.coords_to_xyz(seeds, output)
        seeds = np.atleast_2d(np.stack((x, y, z), axis=-1))

        flines = []
        for seed in seeds:
            xforw = output._integrate_one_way(1, seed, self.rtol, self.atol)
            xback = output._integrate_one_way(-1, seed, self.rtol, self.atol)
            xback = np.flip(xback, axis=1)
            xout = np.vstack((xback.T, xforw.T))
            fline = fieldline.FieldLine(xout[:, 0], xout[:, 1], xout[:, 2], output)

            flines.append(fline)
        return fieldline.FieldLines(flines)


class FortranTracer(PerformanceTracer):
    @deprecated('1.0', message='This class has been renamed to PerformanceTracer as this now does not use Fortran.')
    def __init__(*args, **kwargs):
        super(PerformanceTracer).__init__(*args, **kwargs)
