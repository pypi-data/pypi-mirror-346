#!/usr/bin/env python
u"""
constants.py
Written by Tyler Sutterley (09/2024)
Routines for estimating the harmonic constants for ocean tides

REFERENCES:
    G. D. Egbert and S. Erofeeva, "Efficient Inverse Modeling of Barotropic
        Ocean Tides", Journal of Atmospheric and Oceanic Technology, (2002).

PYTHON DEPENDENCIES:
    numpy: Scientific Computing Tools For Python
        https://numpy.org
        https://numpy.org/doc/stable/user/numpy-for-matlab-users.html
    scipy: Scientific Tools for Python
        https://scipy.org

PROGRAM DEPENDENCIES:
    arguments.py: loads nodal corrections for tidal constituents
    astro.py: computes the basic astronomical mean longitudes

UPDATE HISTORY:
    Updated 09/2024: added bounded options for least squares solvers
    Updated 08/2024: use nodal arguments for all non-OTIS model type cases
    Updated 01/2024: moved to solve subdirectory
    Written 12/2023
"""

from __future__ import annotations

import numpy as np
import scipy.linalg
import scipy.optimize
import pyTMD.arguments

__all__ = [
    'constants'
]

def constants(t: float | np.ndarray,
        ht: np.ndarray,
        constituents: str | list | np.ndarray,
        deltat: float | np.ndarray = 0.0,
        corrections: str = 'OTIS',
        solver: str = 'lstsq',
        bounds: tuple = (-np.inf, np.inf),
        max_iter: int | None = None
    ):
    """
    Estimate the harmonic constants for an elevation time series
    :cite:p:`Egbert:2002ge,Ray:1999vm`

    Parameters
    ----------
    t: float or np.ndarray
        days relative to 1992-01-01T00:00:00
    ht: np.ndarray
        elevation time series (meters)
    constituents: str, list or np.ndarray
        tidal constituent ID(s)
    deltat: float or np.ndarray, default 0.0
        time correction for converting to Ephemeris Time (days)
    corrections: str, default 'OTIS'
        use nodal corrections from OTIS/ATLAS or GOT/FES models
    solver: str, default 'lstsq'
        least squares solver to use

        - ``'lstsq'``: least squares solution
        - ``'gelsy'``: complete orthogonal factorization
        - ``'gelss'``: singular value decomposition (SVD)
        - ``'gelsd'``: SVD with divide and conquer method
        - ``'bvls'``: bounded-variable least-squares
    bounds: tuple, default (None, None)
        Lower and upper bounds on parameters for ``'bvls'``
    max_iter: int or None, default None
        Maximum number of iterations for ``'bvls'``

    Returns
    -------
    amp: np.ndarray
        amplitude of each harmonic constant (meters)
    phase: np.ndarray
        phase of each harmonic constant (degrees)
    """
    # check if input constituents is a string
    if isinstance(constituents, str):
        constituents = [constituents]
    # check that there are enough values for a time series fit
    nt = len(np.atleast_1d(t))
    nc = len(constituents)
    if (nt <= 2*nc):
        raise ValueError('Not enough values for fit')
    # check that the number of time values matches the number of height values
    if (nt != len(np.atleast_1d(ht))):
        raise ValueError('Dimension mismatch between input variables')

    # load the nodal corrections
    # convert time to Modified Julian Days (MJD)
    pu, pf, G = pyTMD.arguments.arguments(t + 48622.0, constituents,
        deltat=deltat, corrections=corrections)

    # create design matrix
    M = []
    # add constant term for mean
    M.append(np.ones_like(t))
    # add constituent terms
    for k,c in enumerate(constituents):
        if corrections in ('OTIS', 'ATLAS', 'TMD3', 'netcdf'):
            amp, ph, omega, alpha, species = \
                pyTMD.arguments._constituent_parameters(c)
            th = omega*t*86400.0 + ph + pu[:,k]
        else:
            th = G[:,k]*np.pi/180.0 + pu[:,k]
        # add constituent to design matrix
        M.append(pf[:,k]*np.cos(th))
        M.append(-pf[:,k]*np.sin(th))
    # take the transpose of the design matrix
    M = np.transpose(M)

    # use a least-squares fit to solve for parameters
    # can optionally use a bounded-variable least-squares fit
    if (solver == 'lstsq'):
        p, res, rnk, s = np.linalg.lstsq(M, ht, rcond=-1)
    elif solver in ('gelsd', 'gelsy', 'gelss'):
        p, res, rnk, s = scipy.linalg.lstsq(M, ht,
            lapack_driver=solver)
    elif (solver == 'bvls'):
        p = scipy.optimize.lsq_linear(M, ht,
            method=solver, bounds=bounds,
            max_iter=max_iter).x

    # calculate amplitude and phase for each constituent
    amp = np.zeros((nc))
    ph = np.zeros((nc))
    # skip over the first indice in the fit (constant term)
    for k,c in enumerate(constituents):
        amp[k] = np.abs(1j*p[2*k+2] + p[2*k+1])
        ph[k] = np.arctan2(-p[2*k+2], p[2*k+1])
    # convert phase to degrees
    phase = ph*180.0/np.pi
    phase[phase < 0] += 360.0

    # return the amplitude and phase
    return (amp, phase)
