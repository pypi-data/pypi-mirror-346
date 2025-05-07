
from collections.abc import Iterable
import cycler

import numpy as np
import pandas
from lemaitre import bandpasses
from matplotlib import pyplot as plt
from ..loglikelihood import LogLikelihood
from ..dataset import TrainingDataset
from .tds import clone
from ..plotting import save_figure

import matplotlib
from scipy.optimize import curve_fit
from matplotlib.animation import FuncAnimation
from bbf.bspline.utils import integ
import pathlib

class ModelPlotter:
    """
    A utility class to plot a smooth, oversampled photometric model along with
    its variance, if available. This is useful for visualizing the fitted model
    and its associated uncertainties over a supernova dataset.
    """
    def __init__(self, model, sn_index, init_pars, variance_model=None):
        """
        Constructor - Initializes the ModelPlotter by evaluating the model and,
        optionally, the error model.

        Parameters:
        -----------
        model : Model (e.g. `nacl.models.salt2.SALT2Like`)
            The photometric model to be plotted. It should support evaluation
            given a set of parameters.

        sn_index : int
            The index of the specific supernova for which the model is being
            plotted, used to select the appropriate parameters from the dataset.

        init_pars : dict
            A dictionary of initial parameters for the model, containing both
            global parameters (e.g., 'M0', 'M1') and supernova-specific
            parameters (e.g., 'X0', 'X1', 'c', 'tmax').

        variance_model : Model, optional
            An optional variance model. If provided, the plotter will also
            compute and display the variance (or error) bands around the model
            predictions.
        """
        self.model = model
        self.tds = model.training_dataset
        self.init_pars = init_pars
        self.variance_model = variance_model
        self._init_local_pars(init_pars, sn_index)

        # evaluate model and variance model
        self.v = self.model(self.pars)
        if variance_model is not None:
            self.v_var = self.variance_model(self.pars)
        else:
            self.v_var = None

    def _init_local_pars(self, init_pars, sn_index):
        """
        Initialize the parameter vector for the selected supernova from a global
        parameter set.

        Parameters:
        -----------
        init_pars : dict
            The initial parameter values for the model, including global and
            supernova-specific parameters.

        sn_index : int
            The index of the supernova in the dataset, used to extract the
            relevant parameters for the current supernova.

        Returns:
        --------
        pars : dict
            A dictionary of parameters specific to the current supernova,
            ready to be used in model evaluation.
        """
        if self.variance_model is not None:
            ll = LogLikelihood(self.model, variance_model=self.variance_model)
            self.pars = ll.pars.copy()
        else:
            self.pars = self.model.init_pars()

        for nm in ['M0', 'M1', 'CL']:
            self.pars[nm].full[:] = init_pars[nm].full[:]
        for nm in ['X0', 'X1', 'c', 'tmax']:
            self.pars[nm].full[0] = init_pars[nm].full[sn_index]
        if 'gamma' in init_pars._struct.slices:
            self.pars['gamma'].full[:] = init_pars['gamma'].full[:]
        if 'gamma_sn' in init_pars._struct.slices and 'gamma_sn' in self.pars._struct.slices:
            self.pars['gamma_sn'].full[0] = init_pars['gamma_sn'].full[sn_index]
        if 'gamma_snake' in init_pars._struct.slices and 'gamma_snake' in self.pars._struct.slices:
            self.pars['gamma_snake'].full[:] = init_pars['gamma_snake'].full[:]
        # else:
        #    self.pars['gamma'].full[:] = 0.

        return self.pars

    def plot(self, band, ax=None, **kwargs):
        """
        Plot the photometric model for a given band, optionally including the
        error model if provided.

        Parameters:
        -----------
        band : str
            The photometric band for which to plot the model (e.g., 'g', 'r').

        ax : matplotlib.axes.Axes, optional
            The matplotlib axes to plot on. If not provided, the current axes
            will be used (plt.gca()).

        **kwargs : dict, optional
            Additional plot parameters, including:
            - phase: bool, whether to plot in phase space (relative to tmax) or
              in MJD (default: False).
            - color: str, the color for the plot (default: 'b').
            - ls: str, the line style for the plot (default: ':').
            - label: str, the label for the plot (default: '').
            - xlabel: str, label for the x-axis (default: None).
            - ylabel: str, label for the y-axis (default: None).
            - title: str, title for the plot (default: None).
            - alpha: float, transparency level for the variance band (default: 0.25).
            - legend: str, location of the legend (default: None).

        Notes:
        ------
        - If a variance model is provided, shaded error bands representing
          ±1σ will be plotted around the model predictions.
        - The method plots calibrated fluxes in the magnitude system specified.
          The fluxes are scaled using the zero points (`zp`) provided in the
          dataset. Since the model predicts fluxes in observer units, it's
          crucial that the `clone()`d dataset has its `zp` values set to zero,
          ensuring that the model generates calibrated fluxes.
        - The `phase` option allows for plotting the time axis either in
          rest-frame phase (relative to tmax) or directly in modified Julian
          dates (MJD).
        """
        if not ax:
            ax = plt.gca()

        phase = kwargs.get('phase', False)
        color = kwargs.get('color', 'b')
        ls = kwargs.get('ls', '-')
        label = kwargs.get('label', '')
        xlabel= kwargs.get('xlabel', None)
        ylabel= kwargs.get('ylabel', None)
        title = kwargs.get('title', None)
        alpha = kwargs.get('alpha', 0.25)
        legend = kwargs.get('legend', None)

        tmax = float(self.tds.sn_data.tmax[0])
        z = float(self.tds.sn_data.z[0])

        idx = self.tds.lc_data.band == band
        if phase:
            xx = (self.tds.lc_data.mjd - tmax) / (1. + z)
            ax.axvline(0., ls=':')
        else:
            xx = self.tds.lc_data.mjd
            ax.axvline(tmax, ls=':')

        y_model = self.v[idx] * np.power(10, -0.4*self.tds.lc_data.zp[idx])
        ax.plot(xx[idx], y_model, color=color, ls=ls, label=label)
        self.ymin, self.ymax = y_model.min(), y_model.max()

        if self.variance_model is not None:
            vm = (self.v[idx] - np.sqrt(self.v_var[idx])) # * np.power(10, -0.4*self.tds.lc_data.zp[idx])
            vp = (self.v[idx] + np.sqrt(self.v_var[idx])) # * np.power(10, -0.4*self.tds.lc_data.zp[idx])
            ax.fill_between(xx[idx], vm, vp, alpha=0.5, color=color)
            self.ymin, self.ymax = vm.min(), vp.max()

        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
        if title is not None:
            ax.set_title(title)
        if legend:
            ax.legend(loc=legend)


def plot_model(model, pars=None,
               bands=['ztfg', 'ztfr', 'ztfi'], # ['STANDARD::B', 'STANDARD::V'],
               magsys='AB', plot_mags=False,
               model_names=None,
               savefig=None,
               output_dir=None,
               ext='.png',
               **kwargs):
    """
    """
    fl = bandpasses.get_filterlib()
    # build a dummy tds
    sne = pandas.DataFrame(np.zeros(1, dtype=TrainingDataset.sn_data_dtype))
    sne['valid'] = 1
    lc_data = []
    for lc, band in enumerate(bands):
        d = pandas.DataFrame(np.zeros(1, dtype=TrainingDataset.lc_data_dtype))
        d['band'] = band
        d['lc'] = lc
        d['magsys'] = magsys
        d['valid'] = 1
        lc_data.append(d)
    lc_data = pandas.concat(lc_data)
    tds = TrainingDataset(sne=sne, lc_data=lc_data, filterlib=fl)

    # expand it into a tds of the kind we use for plotting
    tds = clone(tds, sn=0,
                phase_range=np.arange(-15., 50.+0.1, 0.1))

    # generate a model with the same parameters
    model_to_plot = model.clone(tds)
    model_pars = model_to_plot.init_pars()

    if pars is not None:
        if not isinstance(pars, Iterable):
            pars = [pars]
    else:
        pars = [None]
    if model_names is not None:
        if not isinstance(model_names, Iterable):
            model_names = [model_names]
    else:
         model_names = [''] * len(pars)
    assert len(model_names) == len(pars)

    fig, axes = plt.subplots(figsize=(8,8), nrows=1, ncols=1)
    linestyles = cycler.cycle(['-', '--', ':', '-.'])

    ref_b_band = kwargs.get('ref_b_band', 'swope2::b')
    b_max, b_15 = None, None
    for i, pp in enumerate(pars):
        if pars is not None:
            model_pars['M0'].full[:] = pp['M0'].full
            model_pars['M1'].full[:] = pp['M1'].full
            model_pars['CL'].full[:] = pp['CL'].full
        model_pars['X0'].full[:] = kwargs.get('X0', 1.)
        model_pars['X1'].full[:] = kwargs.get('X1', 0.)
        model_pars['c'].full[:] = kwargs.get('c', 0.)
        model_pars['tmax'].full[:] = kwargs.get('tmax', 0.)
        model_name = '' if model_names is None else model_names[i]
        v = model_to_plot(model_pars)
        mags = -2.5 * np.log10(v)
        ls = next(linestyles)

        for band in bands:
            idx = tds.lc_data.band == band
            wl = tds.lc_data.wavelength[idx].mean()
            color = plt.cm.turbo(int((wl-2000)/(11000.-2000.) * 256))
            if plot_mags:
                axes.plot(tds.lc_data.mjd[idx], mags[idx], ls=ls, color=color, label=f'{model_name}:{band}')
            else:
                axes.plot(tds.lc_data.mjd[idx], v[idx], ls=ls, color=color, label=f'{model_name}:{band}')

            if band.lower() == ref_b_band:
                iidx = idx & ~np.isnan(mags)
                b_peak = mags[iidx].min()
                iidx &= (tds.lc_data.mjd == 15.)
                assert iidx.sum() == 1
                b_15 = mags[iidx][0]
        axes.set_xlabel('mjd [days]')

    if plot_mags:
        axes.invert_yaxis()
        axes.set_ylabel('mag')
        if b_max is not None:
            axes.axhline(b_max, ls=':', color='b')
        if b_15 is not None:
            axes.axhline(b_15, ls=':', color='b')
    else:
        axes.set_ylabel('flux')

    axes.axvline(0., ls=':', color='b')
    axes.axvline(15., ls=':', color='b')
    m_b_at_10Mpc = kwargs.get('m_b_at_10Mpc', -19.5+5*6.)
    axes.plot([0.], [m_b_at_10Mpc], 'ro')
    dm15 = kwargs.get('dm15', 1.)
    axes.plot([15.], [m_b_at_10Mpc+dm15], 'ro')

    plt.legend()

    save_figure(fig, savefig, output_dir, 'model', ext)

    return model_to_plot

import sncosmo
from sksparse.cholmod import cholesky_AAt

def plot_model_comparison(model, pars, 
                          wl_range=None, ph_range=None,
                          savefig=None,
                          output_dir=None,
                          ext='.png'):
    
    basis = model.basis
    
    salt3_source = sncosmo.get_source('salt3')
    phase_salt = salt3_source._phase
    wl_salt = salt3_source._wave
    w, p = np.meshgrid(wl_salt, phase_salt)

    sncosmo_scale = salt3_source._SCALE_FACTOR
    salt3_m0 = salt3_source._model['M0'](phase_salt, wl_salt).ravel() / sncosmo_scale
    salt3_m1 = salt3_source._model['M1'](phase_salt, wl_salt).ravel() / sncosmo_scale
    
    jac = basis.eval(w.ravel(), p.ravel()).tocsr()
    factor = cholesky_AAt(jac.T, beta=1.E-6)
    
    m0_salt3 = factor(jac.T * salt3_m0)
    m1_salt3 = factor(jac.T * salt3_m1)
    
    salt2_source = sncosmo.get_source('salt2', version='2.4')
    phase_salt = salt2_source._phase
    wl_salt = salt2_source._wave
    w, p = np.meshgrid(wl_salt, phase_salt)

    sncosmo_scale = salt2_source._SCALE_FACTOR
    salt2_m0 = salt2_source._model['M0'](phase_salt, wl_salt).ravel() / sncosmo_scale
    salt2_m1 = salt2_source._model['M1'](phase_salt, wl_salt).ravel() / sncosmo_scale
    
    jac = basis.eval(w.ravel(), p.ravel()).tocsr()
    factor = cholesky_AAt(jac.T, beta=1.E-6)
    
    m0_salt2 = factor(jac.T * salt2_m0)
    m1_salt2 = factor(jac.T * salt2_m1)
    
    if wl_range is None:
        wl_range = np.linspace(3300, 8500, 150)
    if ph_range is None:
        ph_range = np.linspace(-12, 31, 100)

    WL, PH = np.meshgrid(wl_range, ph_range)
    J = basis.eval(WL.ravel(), PH.ravel())

    m0_nacl = pars['M0'].full
    m1_nacl = pars['M1'].full

    fig, ax = plt.subplots(ncols = 3, figsize=(10,7))
    
    H_lc, _, _, im0 = ax[0].hist2d(WL.ravel(), PH.ravel(), bins=(150, 100), weights = J @ m0_salt2)
    plt.colorbar(im0)
    ax[0].set_xlabel('wavelength')
    ax[0].set_ylabel('phase')
    ax[0].set_title('SALT2.4 ')
    
    H_lc, _, _, im1 = ax[1].hist2d(WL.ravel(), PH.ravel(), bins=(150, 100), weights = J @ m0_salt3)
    plt.colorbar(im1)
    ax[1].set_xlabel('wavelength')
    ax[1].set_ylabel('phase')
    ax[1].set_title('SALT3')
    
    H_lc, _, _, im2 = ax[2].hist2d(WL.ravel(), PH.ravel(), bins=(150, 100), weights = J @ m0_nacl)
    plt.colorbar(im2)
    ax[2].set_xlabel('wavelength')
    ax[2].set_ylabel('phase')
    ax[2].set_title('NaCl')

    plt.suptitle('M0')
    
    save_figure(fig, savefig, output_dir, 'm0_comparison', ext)
    
    fig, ax = plt.subplots(ncols = 2, figsize=(10,7))
    
    H_lc, _, _, im0 = ax[0].hist2d(WL.ravel(), PH.ravel(), bins=(150, 100), weights = np.abs((J @ m0_salt2 - J @ m0_nacl)/(J @ m0_salt2)), vmin=0, vmax=+1)
    plt.colorbar(im0)
    ax[0].set_xlabel('wavelength')
    ax[0].set_ylabel('phase')
    ax[0].set_title('|(SALT2.4 - NaCl)/SALT2.4|')
    
    H_lc, _, _, im1 = ax[1].hist2d(WL.ravel(), PH.ravel(), bins=(150, 100), weights = np.abs((J @ m0_salt3 - J @ m0_nacl)/(J @ m0_salt3)), vmin=0, vmax=+1)
    plt.colorbar(im1)
    ax[1].set_xlabel('wavelength')
    ax[1].set_ylabel('phase')
    ax[1].set_title('|(SALT3 - NaCl)/SALT3|')

    plt.suptitle('M0')
    
    save_figure(fig, savefig, output_dir, 'm0_differences', ext)
    
    fig, ax = plt.subplots(ncols = 3, figsize=(10,7))
    
    H_lc, _, _, im0 = ax[0].hist2d(WL.ravel(), PH.ravel(), bins=(150, 100), weights = J @ m1_salt2)
    plt.colorbar(im0)
    ax[0].set_xlabel('wavelength')
    ax[0].set_ylabel('phase')
    ax[0].set_title('SALT2.4 ')
    
    H_lc, _, _, im1 = ax[1].hist2d(WL.ravel(), PH.ravel(), bins=(150, 100), weights = J @ m1_salt3)
    plt.colorbar(im1)
    ax[1].set_xlabel('wavelength')
    ax[1].set_ylabel('phase')
    ax[1].set_title('SALT3')
    
    H_lc, _, _, im2 = ax[2].hist2d(WL.ravel(), PH.ravel(), bins=(150, 100), weights = J @ m1_nacl)
    plt.colorbar(im2)
    ax[2].set_xlabel('wavelength')
    ax[2].set_ylabel('phase')
    ax[2].set_title('NaCl')

    plt.suptitle('M1')
    
    save_figure(fig, savefig, output_dir, 'm1_comparison', ext)
    
    fig, ax = plt.subplots(ncols = 2, figsize=(10,7))
    
    H_lc, _, _, im0 = ax[0].hist2d(WL.ravel(), PH.ravel(), bins=(150, 100), weights = np.abs((J @ m1_salt2 - J @ m1_nacl)/(J @ m1_salt2)), vmin=0, vmax=+1)
    plt.colorbar(im0)
    ax[0].set_xlabel('wavelength')
    ax[0].set_ylabel('phase')
    ax[0].set_title('|(SALT2.4 - NaCl)/SALT2.4|')
    
    H_lc, _, _, im1 = ax[1].hist2d(WL.ravel(), PH.ravel(), bins=(150, 100), weights = np.abs((J @ m1_salt3 - J @ m1_nacl)/(J @ m1_salt3)), vmin=0, vmax=+1)
    plt.colorbar(im1)
    ax[1].set_xlabel('wavelength')
    ax[1].set_ylabel('phase')
    ax[1].set_title('|(SALT3 - NaCl)/SALT3|')

    plt.suptitle('M1')
    
    save_figure(fig, savefig, output_dir, 'm1_differences', ext)
    
    
def plot_model_at_phase(model, pars, 
                          wl_range=None, phase=0,
                          savefig=None,
                          output_dir=None,
                          ext='.png'):
      
      
    basis = model.basis
    
    salt3_source = sncosmo.get_source('salt3')
    phase_salt = salt3_source._phase
    wl_salt = salt3_source._wave
    w, p = np.meshgrid(wl_salt, phase_salt)

    sncosmo_scale = salt3_source._SCALE_FACTOR
    salt3_m0 = salt3_source._model['M0'](phase_salt, wl_salt).ravel() / sncosmo_scale
    salt3_m1 = salt3_source._model['M1'](phase_salt, wl_salt).ravel() / sncosmo_scale
    
    jac = basis.eval(w.ravel(), p.ravel()).tocsr()
    factor = cholesky_AAt(jac.T, beta=1.E-6)
    
    m0_salt3 = factor(jac.T * salt3_m0)
    m1_salt3 = factor(jac.T * salt3_m1)
    
    salt2_source = sncosmo.get_source('salt2', version='2.4')
    phase_salt = salt2_source._phase
    wl_salt = salt2_source._wave
    w, p = np.meshgrid(wl_salt, phase_salt)

    sncosmo_scale = salt2_source._SCALE_FACTOR
    salt2_m0 = salt2_source._model['M0'](phase_salt, wl_salt).ravel() / sncosmo_scale
    salt2_m1 = salt2_source._model['M1'](phase_salt, wl_salt).ravel() / sncosmo_scale
    
    jac = basis.eval(w.ravel(), p.ravel()).tocsr()
    factor = cholesky_AAt(jac.T, beta=1.E-6)
    
    m0_salt2 = factor(jac.T * salt2_m0)
    m1_salt2 = factor(jac.T * salt2_m1)
    
    if wl_range is None:
        wl_range = np.linspace(3300, 8500, 200)


    J = basis.eval(wl_range, np.array([phase for i in range(len(wl_range))]))

    m0_nacl = pars['M0'].full
    m1_nacl = pars['M1'].full
    
    fig = plt.figure(figsize=(10,7))
    plt.plot(wl_range, J @ m0_salt2, 'b', label='SALT2.4')
    plt.plot(wl_range, J @ m0_salt3, 'r', label='SALT3')
    plt.plot(wl_range, J @ m0_nacl, 'k', label='NaCl')
    plt.xlabel(r'$\lambda$')
    plt.ylabel('flux')
    plt.title(f'M0 at p={phase}')
    plt.legend()
    save_figure(fig, savefig, output_dir, f'm0_phase_{phase}', ext)

    #plt.figure(figsize=(10,7))
    #plt.plot(wl_range, J @ m1_salt2, 'b', label='SALT2.4')
    #plt.plot(wl_range, J @ m1_salt3, 'r', label='SALT3')
    #plt.plot(wl_range, J @ m1_nacl, 'k', label='NaCl')
    #plt.xlabel(r'$\lambda$')
    #plt.ylabel('flux')
    #plt.title(f'M1 at p={phase}')
    #plt.legend()
      
      
      
      
def plot_color_law(model, pars,
                   wl_range=None, 
                   savefig=None,
                   output_dir=None,
                   ext='.png'):
    if wl_range is None:
        wl_range = np.linspace(3300, 8500, 200)
    
    salt3_source = sncosmo.get_source('salt3')
    salt2_source = sncosmo.get_source('salt2', version='2.4')
    
    fig, ax = plt.subplots(nrows = 2, figsize=(10,7), height_ratios=(3,1), sharex=True)
    
    ax[0].plot(wl_range, -salt2_source.colorlaw(wl_range), 'b', label='SALT2.4')
    ax[0].plot(wl_range, -salt3_source.colorlaw(wl_range), 'r', label='SALT3')
    ax[0].plot(wl_range, model.color_law(wl_range, pars['CL'].full)[0], 'k', label='NaCl')
    ax[1].set_xlabel(r'$\lambda$')
    ax[0].set_ylabel(r'CL($\lambda$)')
    ax[0].set_title('Color Law')
    ax[0].legend()
    
    ax[1].plot(wl_range, -salt2_source.colorlaw(wl_range) - model.color_law(wl_range, pars['CL'].full)[0], 'b', label='SALT2.4 - NaCl')
    ax[1].plot(wl_range, -salt3_source.colorlaw(wl_range) - model.color_law(wl_range, pars['CL'].full)[0], 'r', label='SALT3 - NaCl')
    #ax[0].plot(wl_range, model.colorlaw(wl_range, pars['CL'].full)[0], 'k', label='NaCl')
    ax[1].set_ylabel(r'$\Delta$CL($\lambda$)')
    save_figure(fig, savefig, output_dir, f'CL', ext)
    ax[1].legend()


def plot_dmodel(fm, output_dir=None):
    """
    Parameters:
    fm : FitModel
    """
    ph = np.arange(-25, +101., 1.)
    wl = np.arange(2000., 11010., 10.)
    n_ph, n_wl = len(ph), len(wl)
    X, Y = np.meshgrid(wl, ph)
    wl, ph = X.ravel(), Y.ravel()
    J = fm.model.basis.eval(wl, ph)

    # plot the model itself
    m0 = (J @ fm.pars['M0'].full).reshape((n_ph, n_wl)).T
    plt.figure()
    plt.imshow(m0, aspect='auto', interpolation='none',
              vmin=-0.5, vmax=0.5)

    # plot the model variations as an animation
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16,9),
                          sharex=True, sharey=True)
    pars = fm.initial_pars
    m0 = (J @ pars['M0'].full).reshape((n_ph, n_wl)).T
    img_model = ax[0].imshow(m0, aspect='auto', interpolation='none',
                             extent=(-25, 101, 11000., 2000.),
                             vmin=-0.5, vmax=0.5)
    txt_model = ax[0].text(0.8, 0.9, 'step:   0',
                           horizontalalignment='center',
                           verticalalignment='bottom',
                           transform=ax[0].transAxes)
    fig.colorbar(img_model)

    dpars = fm.minimizer._log[0]['dpars']
    dm0 = (J @ dpars['M0'].full).reshape((n_ph, n_wl)).T
    img_dmodel = ax[1].imshow(dm0, aspect='auto', interpolation='none',
                              extent=(-25, 101, 11000., 2000.),
                              vmin=-1.E-4, vmax=1.E-4)
    txt_dmodel = ax[1].text(0.8, 0.9, 'step:   0',
                            horizontalalignment='center',
                            verticalalignment='bottom',
                            transform=ax[1].transAxes)
    fig.colorbar(img_dmodel)

    ax[0].set_xlabel('restframe phase [days]')
    ax[0].set_xlabel('restframe phase [days]')
    ax[0].set_ylabel('restframe $\lambda [\AA]$')

    # title = ax.set_title('step [0]')
    # fig.colorbar(img)

    frames_model = []
    frames_dmodel = []
    titles = []
    curr_model = m0.copy()
    for i,l in enumerate(fm.minimizer._log):
        dpars = l['dpars']
        dm0 = (J @ dpars['M0'].full).reshape((n_ph, n_wl)).T
        curr_model += dm0
        frames_model.append(curr_model.copy())
        frames_dmodel.append(dm0)
        titles.append(f'step: [{i}]')

    def update(i):
        img_model.set_array(frames_model[i])
        img_dmodel.set_array(frames_dmodel[i])
        txt_model.set_text(titles[i])
        txt_dmodel.set_text(titles[i])
        return [img_model, txt_model,
                img_dmodel, txt_dmodel]

    ani = FuncAnimation(fig, update, frames=len(frames_model), interval=150, blit=True)
    if output_dir is not None:
        if type(output_dir) is str:
            output_dir = pathlib.Path(output_dir)
        ani.save(output_dir.joinpath('model_evolution.mp4'))
    return ani, frames_model


def plot_regularization_grid(fm, 
                             savefig=None,
                             output_dir=None,
                             ext='.png'):
    """
    Parameters:
    fm : FitModel
    """
    ph = np.arange(-50, +101., 1.)
    wl = np.arange(2000., 11010., 10.)
    n_ph, n_wl = len(ph), len(wl)
    X, Y = np.meshgrid(wl, ph)
    wl, ph = X.ravel(), Y.ravel()
    J = fm.model.basis.eval(wl, ph)

    # plot the model itself
    m0 = (J @ fm.pars['M0'].full).reshape((n_ph, n_wl)).T
    m0[np.abs(m0) < 1.E-9] = np.NAN

    fig, axes = plt.subplots(figsize=(16,9), nrows=1, ncols=2, sharex=1, sharey=1)
    im = axes[0].imshow(m0, aspect='auto', interpolation='none',
                        vmin=-0.5, vmax=0.5,
                        extent=(-50., 100., 11000., 2000.),
                        cmap='hsv')
    fig.colorbar(im)
    axes[0].set_title('LC data')

    im2 = axes[1].imshow(m0, aspect='auto', interpolation='none',
                         vmin=-0.5, vmax=0.5,
                         extent=(-50., 100., 11000., 2000.),
                         cmap='hsv')
    axes[1].set_title('SPEC data')
    fig.colorbar(im2)

    # grid of bspline positions
    wl_mean = integ(fm.model.basis.bx, n=1) / integ(fm.model.basis.bx)
    ph_mean = integ(fm.model.basis.by, n=1) / integ(fm.model.basis.by)
    wl, ph = np.meshgrid(wl_mean, ph_mean)
    wl = wl.ravel()
    ph = ph.ravel()
    axes[0].plot(ph, wl, 'k,')
    axes[1].plot(ph, wl, 'k,')

    # which splines are not indexed at all ?
    vm, Jm = fm.model(fm.pars, jac=1)
    j_no_data = np.argwhere(np.bincount(Jm.col, minlength=Jm.shape[1], weights=np.abs(Jm.data)) == 0).ravel()
    i_basis_no_data = np.isin(fm.pars['M0'].indexof(), j_no_data)
    axes[0].plot(ph[i_basis_no_data], wl[i_basis_no_data], 'rx', alpha=0.25)
    axes[1].plot(ph[i_basis_no_data], wl[i_basis_no_data], 'rx', alpha=0.25)

    # overplot the data
    lc_phase = (fm.tds.lc_data.mjd - fm.pars['tmax'].full[fm.tds.lc_data.sn_index]) / (1. + fm.tds.lc_data.z)
    lc_wavelength = fm.tds.lc_data.wavelength / (1. + fm.tds.lc_data.z)
    axes[0].plot(lc_phase, lc_wavelength, color='orange', marker='.', ls='', alpha=0.2)

    sp_phase = (fm.tds.spec_data.mjd - fm.pars['tmax'].full[fm.tds.spec_data.sn_index]) / (1. + fm.tds.spec_data.z)
    sp_wavelength = fm.tds.spec_data.wavelength / (1. + fm.tds.spec_data.z)
    axes[1].plot(sp_phase, sp_wavelength, color='orange', marker='.', ls='', alpha=0.2)

    for i in [0,1]:
        axes[i].set_xlabel('phase [days]')
        axes[i].set_ylabel('$\\lambda [\AA]$')
    save_figure(fig, savefig, output_dir, f'model_regularized', ext)
    return Jm, j_no_data

def plot_regularization_map(model,
                            pars_full,
                            tds,
                            savefig=None,
                            output_dir=None,
                            ext='.png'):
    """
    Plotting the regularization map
    """
    pars = pars_full.copy()
    pars.fix()
    pars.release('M0')
    
    n_lc = len(tds.lc_data)
    
    _, J = model(pars, jac=True)
    
    J = J.toarray()
    
    J_lc = J[:n_lc]
    J_sp = J[n_lc:]
    
    J_lc[J_lc>0] = 1
    J_lc.astype(int)
    
    # Splines that see data
    N_lc = J_lc.sum(axis=0)
    
    # 2D histogram
    fig = plt.figure(figsize=(10,7))
    plt.imshow(N_lc.reshape(model.basis.by.nj, model.basis.bx.nj), aspect='auto')
    plt.colorbar()
    plt.title(r'$N_{pl}$ for LC')
    save_figure(fig, savefig, output_dir, f'regularization_map_lc', ext)
    
    J_sp[J_sp>0] = 1
    J_sp.astype(int)
    
    # Splines that see data
    N_sp = J_sp.sum(axis=0)
    
    # 2D histogram
    fig = plt.figure(figsize=(10,7))
    plt.imshow(N_sp.reshape(model.basis.by.nj, model.basis.bx.nj), aspect='auto')
    plt.colorbar()
    plt.title(r'$N_{pl}$ for SPEC')
    save_figure(fig, savefig, output_dir, f'regularization_map_sp', ext)    
