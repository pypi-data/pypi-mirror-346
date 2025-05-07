"""
"""

import numpy as np
from ..dataset import TrainingDataset


def clone(tds, sn, phase_range=(-25, 51., 1.)):
    """Create a clone of the `TrainingDataset` object for a specific supernova,
    allowing for a different (finer) sampling of the light curves.

    This function is primarily used to generate data for plotting models like
    NaCl / SALT2 over observed data points, with the option to adjust the phase
    grid of the light curves, to plot smoother models.

    Parameters:
    -----------
    tds : TrainingDataset
        The original training dataset containing the supernova data.

    sn : str
        The identifier of the supernova to clone.

    phase_range : tuple, optional
        A tuple specifying the phase range (start, end, step) for generating
        new light curve data. Default is (-25, 51, 1).

    Returns:
    --------
    TrainingDataset
        A new `TrainingDataset` object containing cloned data for the specified
        supernova. The lightcurve data is sampled over the new phase grid, and
        zero-point (zp) values are set to zero. The magnitude system is
        preserved from the original dataset.

    Notes:
    ------
    - This method verifies that all magnitudes in the lightcurve data are in the
      same magnitude system before proceeding.
    - The model predicts observer fluxes (not calibrated fluxes). In the
      plotting routine, model fluxes need to be renormalized to calibrated
      (generally AB) fluxes.
    - If any of the lightcurve, spectral, or spectrophotometric data are absent
      in the original dataset, they will be set to `None` in the cloned object.
    """
    # sn metadata
    sn_data = tds.sn_data.nt[tds.sn_data.sn == sn]

    # lightcurve data
    if tds.lc_data is not None:
        lc_data = tds.lc_data.nt[tds.lc_data.sn == sn]

        # figure out which magnitude system to use
        magsys = np.unique(lc_data.magsys)
        assert len(magsys) == 1

        tmax = float(sn_data.tmax)
        z = float(sn_data.z)
        phase = np.arange(*phase_range)
        mjd = phase * (1.+z) + tmax
        N = len(mjd)
        l = []
        for b in np.unique(lc_data.band):
            d = lc_data[lc_data.band == b]
            Z = np.full(len(mjd), d[0])
            Z['mjd'] = mjd
            Z['flux'] = 0.
            Z['fluxerr'] = 0.
            Z['valid'] = 1
            # we want the model to predict AB (normalized) fluxes
            # so, explicitely set the zero points to zero
            Z['zp'] = 0.
            Z['magsys'] = magsys[0]
            l.append(Z)
        lc_data = np.rec.array(np.hstack(l))
    else:
        lc_data = None

    if tds.spec_data is not None:
        spec_data = tds.spec_data.nt[tds.spec_data.sn == sn]
    else:
        spec_data = None
    if tds.spectrophotometric_data is not None:
        spectrophotometric_data = tds.spectrophotometric_data.nt[tds.spectrophotometric_data.sn == sn]
    else:
          spectrophotometric_data = None


    tds = TrainingDataset(sn_data, lc_data=lc_data,
                          spec_data=None,
                          spectrophotometric_data=None,
                          basis=tds.basis,
                          filterlib=tds.filterlib)

    return tds
