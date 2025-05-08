import pathlib
import functools

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import scipy.integrate
from sympy import acos, asin, cos, lambdify, sin
from sympy.abc import x

import astropy.units as u

import sunpy.map

import sunkit_magex.pfss.analytic as analytic
import sunkit_magex.pfss.utils

result_dir = (pathlib.Path(__file__) / '..' / 'results').resolve()
pi = np.pi * u.rad


def theta_phi_grid(nphi, ns):
    # Return a theta, phi grid with a given number of points
    phi = np.linspace(0, 2 * np.pi, nphi)
    s = np.linspace(-1, 1, ns)
    s, phi = np.meshgrid(s, phi)
    theta = np.arccos(s)
    return theta * u.rad, phi * u.rad


def pfsspy_output(nphi, ns, nrho, rss, l, m):
    assert l >= 1, 'l must be >= 1'
    # Return the sunkit_magex.pfss solution for given input parameters
    theta, phi = theta_phi_grid(nphi, ns)

    br_in = analytic.Br(l, m, rss)(1, theta, phi)

    header = sunkit_magex.pfss.utils.carr_cea_wcs_header('2020-1-1', br_in.shape)
    input_map = sunpy.map.Map((br_in.T, header))

    pfss_input = sunkit_magex.pfss.Input(input_map, nrho, rss)
    return sunkit_magex.pfss.pfss(pfss_input)


def brss_pfss(nphi, ns, nrho, rss, l, m):
    # Return the radial component of the source surface mangetic field
    # for given input parameters
    pfss_out = pfsspy_output(nphi, ns, nrho, rss, l, m)
    return pfss_out.bc[0][:, :, -1].T.astype(float)


def brss_analytic(nphi, ns, rss, l, m):
    # Return the analytic solution for given input parameters
    theta, phi = theta_phi_grid(nphi, ns)
    return analytic.Br(l, m, rss)(rss, theta, phi).T


def open_flux_analytic(l, m, zss):
    """
    Calculate analytic unsigned open flux for spherical harmonic (*l*, *m*) and
    a source surface radius of *zss*.
    """
    Br = analytic.Br(l, m, zss)
    Br = functools.partial(Br, zss)

    def absBr(theta, phi):
        return np.abs(Br(theta * u.rad, phi * u.rad)) * np.sin(theta)

    res = scipy.integrate.nquad(absBr, ranges=[[0, np.pi], [0, 2 * np.pi]])
    return res[0]


def open_flux_numeric(l, m, zss, nrho):
    """
    Calculate numerical unsigned open flux for spherical harmonic (*l*, *m*)
    a source surface radius of *zss* and *nrho* grid points in the radial
    direction.
    """
    nphi = 360
    ns = 180
    br = brss_pfss(nphi, ns, nrho, zss, l, m)
    return np.sum(np.abs(br)) * (4 * np.pi) / nphi / ns


@u.quantity_input
def fr(r: u.m, rss: u.m, l):
    rho = r / rss
    return ((rho**l * (2*l+1)) /
            ((l * rho**(2*l+1)) + l+1))**(2 / (l+1))


flm_dict = {(1, 0): [sin(x)**2, asin(x**(1/2))],
            (1, 1): [cos(x)**2, acos(x**(1/2))],
            (2, 1): [cos(2*x), acos(x) / 2],
            (2, 2): [cos(x)**2, acos(abs(x)**(1/2))],
            (3, 2): [3 * cos(2*x) + 1, acos((x - 1) / 3) / 2],
            (3, 3): [cos(x)**2, acos(abs(x)**(1/2))]}

glm_dict = {(1, 1): sin(x) / cos(x),
            (2, 1): sin(x) / abs(cos(2*x))**(1/2),
            (2, 2): (sin(x) / cos(x))**(2),
            (3, 2): sin(x)**2 / (2 - 3 * sin(x)**2),
            (3, 3): (sin(x) / cos(x))**(3)}


@u.quantity_input
def theta_fline_coords(r: u.m, rss: u.m, l, m, theta: u.rad):
    """
    r :
        Radial point.
    rss :
        Source surface radius.
    l, m : int
        Spherical harmonic numbers.
    theta :
        Source surface latitude, in range [-pi/2, pi/2]

    Returns
    -------
    theta_fline :
        Theta field line coordinates, in range [-pi/2, pi/2]
    """
    theta = pi / 2 - theta
    flm = lambdify(x, flm_dict[(l, abs(m))][0], "numpy")
    flm_inv = lambdify(x, flm_dict[(l, abs(m))][1], "numpy")
    theta_out = flm_inv(flm(theta) * fr(r, rss, l))
    theta_out = pi / 2 - theta_out
    theta_out *= np.sign(theta_out) * np.sign(pi / 2 - theta)
    return theta_out


@u.quantity_input
def phi_fline_coords(r: u.m, rss: u.m, l, m, theta_ss: u.rad, phi: u.rad):
    """
    Parameters
    ----------
    r :
        Radial point.
    rss :
        Source surface radius.
    l, m : int
        Spherical harmonic numbers.
    theta_ss, phi :
        Source surface latitude (in range [-pi/2, pi/2]) and longitude.

    Returns
    -------
    phi :
        Phi coordinates of field line(s).
    """
    theta_fline = theta_fline_coords(r, rss, l, m, theta_ss)
    theta_fline = pi / 2 - theta_fline
    theta_ss = pi / 2 - theta_ss
    if m == 0:
        phi_out = phi
    else:
        glm = lambdify(x, glm_dict[(l, abs(m))], "numpy")
        glm_ratio = glm(theta_ss) / glm(theta_fline)
        if m > 0:
            # arcsin gives values in range [-pi/2, pi/2]
            phi_out = np.arcsin(glm_ratio * np.sin(m * phi)) / m
            phi_out = unwrap_sin(phi, phi_out, m)
        elif m < 0:
            # arccos gives values in range [0, pi]
            phi_out = np.arccos(glm_ratio * np.cos(m * phi)) / m
            phi_out = unwrap_cos(phi, phi_out, m)
    return phi_out


def unwrap_sin(phi_in, phi_out, m):
    phi_0 = pi / (2 * m)
    for n in range(m * 2 + 1):
        lower_lim = -phi_0 + n * pi / m
        upper_lim = phi_0 + n * pi / m
        mask = (phi_in > lower_lim) & (phi_in < upper_lim)
        if n % 2 == 1:
            phi_out[mask] *= -1
        phi_out[mask] += n * pi / m

    return phi_out


def unwrap_cos(phi_in, phi_out, m):
    m = abs(m)
    for n in range(m * 2):
        lower_lim = n * pi / m
        upper_lim = (n + 1) * pi / m
        mask = (phi_in > lower_lim) & (phi_in < upper_lim)
        if n % 2 == 0:
            phi_out[mask] *= -1
        else:
            phi_out[mask] += pi / m
        phi_out[mask] += n * pi / m

    return phi_out


class LMAxes:
    """
    Wrapper for a set of subplots spanning spherical harmonic numbers.
    """
    def __init__(self, nl):
        self.nl = nl

        self.fig = plt.figure(figsize=(10, 4))
        self.grid = self.fig.add_gridspec(ncols=2 * nl + 1, nrows=nl)
        self.axs = np.empty((nl, 2 * nl + 1), dtype=object)
        self.all_axs = []   # List of all axs
        for l in range(1, nl+1):
            for m in range(-l, l+1):
                idx = self.grid_idx(l, m)
                ax = self.fig.add_subplot(self.grid[idx])
                self.axs[idx] = ax
                self.all_axs.append(ax)

                ax.xaxis.set_major_formatter(mticker.NullFormatter())
                ax.yaxis.set_major_formatter(mticker.NullFormatter())
                for minor in [True, False]:
                    ax.xaxis.set_ticks([], minor=minor)
                    ax.yaxis.set_ticks([], minor=minor)
                for spine in ax.spines:
                    ax.spines[spine].set_visible(False)

                if l == nl:
                    ax.set_xlabel(f'm = {m}')
                if m == -l:
                    ax.set_ylabel(f'l = {l}')

    def grid_idx(self, l, m):
        return l-1, m+self.nl

    def __getitem__(self, item):
        l, m = item
        idx = self.grid_idx(l, m)
        return self.axs[idx]
