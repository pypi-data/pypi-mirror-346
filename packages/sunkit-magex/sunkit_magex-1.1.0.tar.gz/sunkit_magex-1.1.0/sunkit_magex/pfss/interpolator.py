"""
Interpolator functions

This module contains a version of scipy.interpolate.RegularGridInterpolator,
which has been edited for performance.

.. warning::

    THE CODE HERE IS LIABLE TO CHANGE/BREAK AT ANY TIME.
    Do not use this code outside of sunkit_magex.pfss.
"""
import itertools

import numpy as np


class RegularGridInterpolator:
    """
    Interpolation on a regular grid in arbitrary dimensions
    The data must be defined on a regular grid; the grid spacing however may be
    uneven.  Linear interpolation is performed.
    Parameters
    ----------
    points : tuple of ndarray of float, with shapes (m1, ), ..., (mn, )
        The points defining the regular grid in n dimensions.
    values : array_like, shape (m1, ..., mn, ...)
        The data on the regular grid in n dimensions.
    fill_value : number, optional
        If provided, the value to use for points outside of the
        interpolation domain. If None, values outside
        the domain are extrapolated.
    """
    # this class is based on code originally programmed by Johannes Buchner,
    # see https://github.com/JohannesBuchner/regulargrid

    def __init__(self, points, values):

        fill_value = np.nan
        if not hasattr(values, 'ndim'):
            # allow reasonable duck-typed values
            values = np.asarray(values)

        if len(points) > values.ndim:
            raise ValueError(f"There are {len(points)} point arrays, but "
                             "values has {values.ndim} dimensions")

        if hasattr(values, 'dtype') and hasattr(values, 'astype'):
            if not np.issubdtype(values.dtype, np.inexact):
                values = values.astype(float)

        self.fill_value = fill_value

        for i, p in enumerate(points):
            if not np.all(np.diff(p) > 0.):
                raise ValueError(f"The points in dimension {i} must be strictly "
                                 "ascending")
            if not np.asarray(p).ndim == 1:
                raise ValueError(f"The points in dimension {i} must be "
                                 "1-dimensional")
            if not values.shape[i] == len(p):
                raise ValueError(f"There are {len(p)} points and {values.shape[i]} "
                                 "values in dimension {i}")
        self.grid = tuple([np.asarray(p) for p in points])
        self.values = values

    def __call__(self, xi):
        """
        Interpolation at coordinates
        Parameters
        ----------
        xi : ndarray of shape (..., ndim)
            The coordinates to sample the gridded data at
        """
        ndim = len(self.grid)
        xi = _ndim_coords_from_arrays(xi, ndim=ndim)
        if xi.shape[-1] != len(self.grid):
            raise ValueError("The requested sample points xi have dimension "
                             f"{xi.shape[1]}, but this RegularGridInterpolator has "
                             f"dimension {ndim}")

        xi_shape = xi.shape
        xi = xi.reshape(-1, xi_shape[-1])

        indices, norm_distances, out_of_bounds = _find_indices(xi.T, self.grid)
        edges = np.array(list(itertools.product(*[[i, i + 1] for i in indices])))[:, :, 0]
        result = _evaluate_linear(self.values, indices, norm_distances, edges)
        if self.fill_value is not None:
            result[out_of_bounds] = self.fill_value

        return result.reshape(xi_shape[:-1] + self.values.shape[ndim:])


def _find_indices(xi, grid):
    # find relevant edges between which xi are situated
    indices = []
    # compute distance to lower edge in unity units
    norm_distances = []
    # check for out of bounds xi
    out_of_bounds = np.zeros((xi.shape[1]), dtype=bool)
    # iterate through dimensions
    for x, grid in zip(xi, grid):
        i = np.searchsorted(grid, x) - 1
        i[i < 0] = 0
        i[i > grid.size - 2] = grid.size - 2
        indices.append(i)
        norm_distances.append((x - grid[i]) /
                              (grid[i + 1] - grid[i]))
        out_of_bounds += x < grid[0]
        out_of_bounds += x > grid[-1]

    return indices, norm_distances, out_of_bounds


def _evaluate_linear(values_in, indices, norm_distances, edges):
    # slice for broadcasting over trailing dimensions in self.values
    vslice = (slice(None),) + (None,) * (values_in.ndim - len(indices))
    values = 0.
    edges = itertools.product(*[[i, i + 1] for i in indices])
    for edge_indices in edges:
        weight = 1.
        for ei, i, yi in zip(edge_indices, indices, norm_distances):
            weight *= np.where(ei == i, 1 - yi, yi)
        values += np.asarray(values_in[edge_indices]) * weight[vslice]
    return values


def _ndim_coords_from_arrays(points, ndim=None):
    """
    Convert a tuple of coordinate arrays to a (..., ndim)-shaped array.
    """
    if isinstance(points, tuple) and len(points) == 1:
        # handle argument tuple
        points = points[0]
    if isinstance(points, tuple):
        p = np.broadcast_arrays(*points)
        n = len(p)
        for j in range(1, n):
            if p[j].shape != p[0].shape:
                raise ValueError("coordinate arrays do not have the same shape")
        points = np.empty(p[0].shape + (len(points),), dtype=float)
        for j, item in enumerate(p):
            points[..., j] = item
    else:
        points = np.asanyarray(points)
        if points.ndim == 1:
            if ndim is None:
                points = points.reshape(-1, 1)
            else:
                points = points.reshape(-1, ndim)
    return points
