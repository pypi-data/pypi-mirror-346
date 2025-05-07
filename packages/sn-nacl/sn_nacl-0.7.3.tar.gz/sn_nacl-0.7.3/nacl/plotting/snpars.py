"""plot the SN related parameters
"""

import numpy as np
import matplotlib.pyplot as plt
from ..plotting import save_figure
from scipy.optimize import curve_fit


def plot_sn_pars_vs_init(model, pars, covmat=None,
                         savefig=None,
                         output_dir=None,
                         ext='.png'):
    """
    """
    tds = model.training_dataset

    sig = pars.copy()
    sig.full[:] = 0.
    if covmat is not None:
        sig.free = np.sqrt(covmat.diagonal())
        #    else:
        #        sig.free = 1.E-6

    fig, axes = plt.subplots(figsize=(12,12), nrows=2, ncols=2)
    fig.suptitle('SN parameters')
    axes[0,0].errorbar(tds.sn_data.x0, pars['X0'].full[tds.sn_data.sn_index],
                       yerr=sig['X0'].full[tds.sn_data.sn_index],
                       ls='', color='gray', marker=',', alpha=0.5)
    axes[0,0].scatter(tds.sn_data.x0, pars['X0'].full[tds.sn_data.sn_index],
                      c=tds.sn_data.z, s=5)
    axes[0,0].set_xlabel('$x_0$ [init]')
    axes[0,0].set_ylabel('$x_0$ [reco]')

    axes[0,1].errorbar(tds.sn_data.x1, pars['X1'].full[tds.sn_data.sn_index],
                       yerr=sig['X1'].full[tds.sn_data.sn_index],
                       ls='', color='gray', marker=',', alpha=0.5)
    axes[0,1].scatter(tds.sn_data.x1, pars['X1'].full[tds.sn_data.sn_index],
                      c=tds.sn_data.z, s=5)
    axes[0,1].set_xlabel('$x_1$ [init]')
    axes[0,1].set_ylabel('$x_1$ [reco]')

    axes[1,0].errorbar(tds.sn_data.col, pars['c'].full[tds.sn_data.sn_index],
                       yerr=sig['c'].full[tds.sn_data.sn_index],
                       ls='', color='gray', marker=',', alpha=0.5)
    axes[1,0].scatter(tds.sn_data.col, pars['c'].full[tds.sn_data.sn_index],
                      c=tds.sn_data.z, s=5)
    axes[1,0].set_xlabel('$c$ [init]')
    axes[1,0].set_ylabel('$c$ [reco]')

    axes[1,1].errorbar(tds.sn_data.tmax, pars['tmax'].full[tds.sn_data.sn_index],
                       yerr=sig['tmax'].full[tds.sn_data.sn_index],
                       ls='', color='gray', marker=',', alpha=0.5)
    axes[1,1].scatter(tds.sn_data.tmax, pars['tmax'].full[tds.sn_data.sn_index],
                      c=tds.sn_data.z, s=5)
    axes[1,1].set_xlabel('$t_{max}$ [init]')
    axes[1,1].set_ylabel('$t_{max}$ [reco]')

    save_figure(fig, savefig, output_dir, 'sn_pars_vs_init', ext)


def plot_sn_pars_minus_init(model, pars, covmat=None,
                            savefig=None,
                            output_dir=None,
                            ext='.png',
                            sn_index=False,
                            use_truth=False):
    """
    """
    tds = model.training_dataset

    sig = pars.copy()
    sig.full[:] = 0.
    if covmat is not None:
        sig.free = np.sqrt(covmat.diagonal())
    else:
        sig.free = 1.E-6

    if sn_index:
        xx = tds.sn_data.sn_index
    else:
        xx = tds.sn_data.z
    xlabel = 'sn_index' if sn_index else '$z$'
    ylabel_suffix = ' [reco-truth]' if use_truth else ' [reco-init]'

    fig, axes = plt.subplots(figsize=(12,12), nrows=2, ncols=2)
    fig.suptitle('SN parameters')
    #axes[0,0].plot(tds.sn_data.z, pars['X0'].full[tds.sn_data.sn_index]/tds.sn_data.x0, 'b.')
    x0 = tds.sn_data.nt['x0_true'] if use_truth else tds.sn_data.x0
    axes[0,0].errorbar(xx,
                       pars['X0'].full[tds.sn_data.sn_index]/x0,
                       yerr=sig['X0'].full[tds.sn_data.sn_index]/x0,
                       ls='', marker='.', color='k')
    axes[0,0].set_xlabel(xlabel)
    axes[0,0].set_ylabel('$x_0$' + ylabel_suffix)

    #axes[0,1].plot(tds.sn_data.z, pars['X1'].full[tds.sn_data.sn_index]-tds.sn_data.x1, 'b.')
    x1 = tds.sn_data.nt['x1_true'] if use_truth else tds.sn_data.x1
    axes[0,1].errorbar(xx,
                       pars['X1'].full[tds.sn_data.sn_index]-x1,
                       yerr=sig['X1'].full[tds.sn_data.sn_index],
                       ls='', marker='.', color='k')

    axes[0,1].set_xlabel(xlabel)
    axes[0,1].set_ylabel('$x_1$' + ylabel_suffix)

    #axes[1,0].plot(tds.sn_data.z, pars['c'].full[tds.sn_data.sn_index]-tds.sn_data.col, 'b.')
    col = tds.sn_data.nt['c_true'] if use_truth else tds.sn_data.col
    axes[1,0].errorbar(xx,
                       pars['c'].full[tds.sn_data.sn_index]-col,
                       yerr=sig['c'].full[tds.sn_data.sn_index],
                       ls='', marker='.', color='k')
    axes[1,0].set_xlabel(xlabel)
    axes[1,0].set_ylabel('$c$' + ylabel_suffix)

    #axes[1,1].plot(tds.sn_data.z, pars['tmax'].full[tds.sn_data.sn_index]-tds.sn_data.tmax, 'b.')
    tmax = tds.sn_data.nt['tmax'] if use_truth else tds.sn_data.tmax
    axes[1,1].errorbar(xx,
                       pars['tmax'].full[tds.sn_data.sn_index]-tmax,
                       yerr=sig['tmax'].full[tds.sn_data.sn_index],
                       ls='', marker='.', color='k')
    axes[1,1].set_xlabel(xlabel)
    axes[1,1].set_ylabel('$t_{max}$' + ylabel_suffix)

    save_figure(fig, savefig, output_dir, 'sn_pars_minus_init', ext)


def f(x, a, b):
    return a*x+b

def x1_comparison(data, 
                  sigma_x1=None,
                  savefig=None,
                  output_dir=None,
                  ext='.png'):
    """
    Compares the initial and final x1 values
    and finds the linear relation between them
    
    Parameters:
    -----------
    data : pandas.DataFrame
        nacl output
        
    sigma_x1 : numpy.ndarray
        (optional) x1 uncertainties
    """
    plt.figure(figsize=(10,7))
    plt.plot(data['x1_init'], data['x1'], 'r.')
    plt.xlabel('x1 initial')
    plt.ylabel('x1 fitted')
    
    popt, pcov = curve_fit(f, data['x1_init'].to_numpy(), data['x1'].to_numpy(), sigma = sigma_x1)
    
    xplot = np.linspace(np.min(data['x1_init']), np.max(data['x1_init']), 50)
    plt.plot(xplot, f(xplot, *popt), 'k', label=f'a={popt[0]:.2f}  b={popt[1]:.2f}')
    plt.legend()
    plt.title('x1 comparison')
    save_figure(fig, savefig, output_dir, 'x1_comparison', ext)

def c_comparison(data, 
                 sigma_c=None,
                 savefig=None,
                 output_dir=None,
                 ext='.png'):
    """
    Compares the initial and final c values
    and finds the linear relation between them
    
    Parameters:
    -----------
    data : pandas.DataFrame
        nacl output
        
    sigma_c : numpy.ndarray
        (optional) c uncertainties
    """
    plt.figure(figsize=(10,7))
    plt.plot(data['c_init'], data['c'], 'b.')
    plt.xlabel('c initial')
    plt.ylabel('c fitted')
    
    popt, pcov = curve_fit(f, data['c_init'].to_numpy(), data['c'].to_numpy(), sigma = sigma_c)
    
    xplot = np.linspace(np.min(data['c_init']), np.max(data['c_init']), 50)
    plt.plot(xplot, f(xplot, *popt), 'k', label=f'a={popt[0]:.2f}  b={popt[1]:.2f}')
    plt.legend()
    plt.title('c comparison')
    save_figure(fig, savefig, output_dir, 'c_comparison', ext)
    
    
    
# def plot_sn_pars_minus_init(tds, model, pars, covmat=None):
#     """
#     """
#     sig = pars.copy()
#     if covmat is not None:
#         sig.full[:] = np.sqrt(np.diag(covmat))
#     else:
#         sig.full[:] = 1.E-6

#     fig, axes = plt.subplots(figsize=(12,12), nrows=2, ncols=2)
#     fig.suptitle('SN parameters')
#     axes[0,0].plot(tds.sn_data.z, pars['X0'].full[tds.sn_data.sn_index]/tds.sn_data.x0, 'b.')
#     axes[0,0].errorbar(tds.sn_data.z,
#                        pars['X0'].full[tds.sn_data.sn_index]/tds.sn_data.x0,
#                        yerr=sig['X0'].full[tds.sn_data.sn_index],
#                        ls='', marker='.', color='k')
#     axes[0,0].set_xlabel('$z$')
#     axes[0,0].set_ylabel('$x_0$ [reco-init]')

#     axes[0,1].plot(tds.sn_data.z, pars['X1'].full[tds.sn_data.sn_index]-tds.sn_data.x1, 'b.')
#     axes[0,1].errorbar(tds.sn_data.z,
#                        pars['X1'].full[tds.sn_data.sn_index]-tds.sn_data.x1,
#                        yerr=sig['X1'].full[tds.sn_data.sn_index],
#                        ls='', marker='.', color='k')

#     axes[0,1].set_xlabel('$z$')
#     axes[0,1].set_ylabel('$x_1$ [reco-init]')

#     axes[1,0].plot(tds.sn_data.z, pars['c'].full[tds.sn_data.sn_index]-tds.sn_data.col, 'b.')
#     axes[1,0].errorbar(tds.sn_data.z,
#                        pars['c'].full[tds.sn_data.sn_index]-tds.sn_data.col,
#                        yerr=sig['c'].full[tds.sn_data.sn_index],
#                        ls='', marker='.', color='k')
#     axes[1,0].set_xlabel('$z$')
#     axes[1,0].set_ylabel('$c$ [reco-init]')

#     axes[1,1].plot(tds.sn_data.z, pars['tmax'].full[tds.sn_data.sn_index]-tds.sn_data.tmax, 'b.')
#     axes[1,1].errorbar(tds.sn_data.z,
#                        pars['tmax'].full[tds.sn_data.sn_index]-tds.sn_data.tmax,
#                        yerr=sig['tmax'].full[tds.sn_data.sn_index],
#                        ls='', marker='.', color='k')
#     axes[1,1].set_xlabel('$z$')
#     axes[1,1].set_ylabel('$t_{max}$ [reco-init]')
