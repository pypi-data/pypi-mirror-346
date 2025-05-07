"""light curve plotting routines
"""
import logging
import  numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from . import save_figure, get_band_order
from . import tds as tdsutils
from .model import ModelPlotter
from scipy.optimize import curve_fit

def plot_sn_lightcurves(model, pars,
                        sn_index=None, sn=None,
                        snake=None,
                        phase=False,
                        savefig=None,
                        output_dir=None,
                        ext='.png'):
    """plot the lightcurves of a given SN, along with the model

    .. todo:
      allow more models to be plotted
    """
    tds = model.training_dataset

    sel = None
    if sn is not None:
        sel = tds.lc_data.sn == sn
        sn_index = tds.sn_data.sn_map[sn]
    elif sn_index is not None:
        sel = tds.lc_data.sn_index == sn_index
        sn = tds.sn_data.sn_set[sn_index]
        print(sn)

    assert sel is not None

    bands = np.unique(tds.lc_data.band[sel]).tolist()
    bands.sort(key=get_band_order)
    nrows = len(bands)

    sn_idx = tds.sn_data.sn == sn
    tmax = float(tds.sn_data.tmax[sn_idx])
    z = float(tds.sn_data.z[sn_idx])

    # clone the dataset and instantiate a temp model
    t = tdsutils.clone(tds, sn)
    m = model.clone(t)
    # snk = snake.__class__(m) if snake is not None else None
    snk = snake.clone(m) if snake is not None else None
    p = ModelPlotter(m, sn_index, pars, variance_model=snk)

    # plots
    fig, axes = plt.subplots(nrows=nrows, ncols=1,
                             figsize=(8,12),
                             sharex=True)
    for i,b in enumerate(bands):
        idx = sel & (tds.lc_data.band == b)
        wl = tds.lc_data.wavelength[idx].mean()
        color = plt.cm.rainbow(int((wl-2000)/(11000.-2000.) * 256))

        if phase:
            xx = (tds.lc_data.mjd[idx] - tmax) / (1. + z)
            axes[i].axvline(0., ls=':')
            axes[i].set_xlim(min(xx.min()-2, -10), max(xx.max()+2, +40))
        else:
            xx = tds.lc_data.mjd[idx]
            axes[i].axvline(tmax, ls=':')
            axes[i].set_xlim(min(xx.min()-2, tmax-10), max(xx.max()+2, tmax+40))

        # we plot the calibrated fluxes. Therefore, we rescale them, using
        # the zero points reported with each flux measurement in the TrainingDataset
        y = tds.lc_data.flux[idx] * np.power(10, -0.4*tds.lc_data.zp[idx])
        yerr = tds.lc_data.fluxerr[idx] * np.power(10, -0.4*tds.lc_data.zp[idx])
        axes[i].errorbar(xx, y, yerr=yerr, ls='', marker='.', color=color)

        if p:
            p.plot(b, ax=axes[i],
                   color=color,
                   phase=phase,
                   ylabel=b)

    if phase:
        axes[-1].set_xlabel('phase [restframe days]')
    else:
        axes[-1].set_xlabel('mjd [days]')

    plt.subplots_adjust(hspace=0.05)
    fig.suptitle(f'{sn} @ z={z:4.3}')

    save_figure(fig, savefig, output_dir, 'sn_lightcurves', ext)


def plot_sn_lightcurves_compact(model, pars,
                                sn_index=None, sn=None,
                                snake=None,
                                static_snake=None,
                                phase=False,
                                residuals=False,
                                pulls=False,
                                ax=None,
                                model_val=None,
                                snake_val=None,
                                savefig=None,
                                output_dir=None,
                                ext='.png'):
    """plot the lightcurves of a given SN, along with the model, all bands in a single axis

    """
    tds = model.training_dataset

    sel = None
    if sn is not None:
        sel = tds.lc_data.sn == sn
        sn_index = tds.sn_data.sn_map[sn]
    elif sn_index is not None:
        sel = tds.lc_data.sn_index == sn_index
        sn = tds.sn_data.sn_set[sn_index]

    assert sel is not None

    bands = np.unique(tds.lc_data.band[sel]).tolist()
    bands.sort(key=get_band_order)

    sn_idx = tds.sn_data.sn == sn
    tmax = float(tds.sn_data.tmax[sn_idx])
    z = float(tds.sn_data.z[sn_idx])

    # do we need the original model values ?
    if residuals or pulls:
        if model_val is None:
            model_val = model(pars)
            model_val = model_val[:len(tds.lc_data)]
        if snake_val is None and snake is not None:
            snake_val = snake(pars)
            snake_val = snake_val[:len(tds.lc_data)]

    # clone the dataset and instantiate a temp model
    if not residuals and not pulls:
        t = tdsutils.clone(tds, sn)
        m = model.clone(t)
        snk = snake.clone(m) if snake is not None else None
        p = ModelPlotter(m, sn_index, pars,
                                        variance_model=snk)
    else:
        p = None

    # plots
    if ax is None:
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()

    xmin, xmax, ymin, ymax = [], [], [], []
    for i, b in enumerate(bands):
        idx = sel & (tds.lc_data.band == b)
        wl = tds.lc_data.wavelength[idx].mean()
        color = plt.cm.turbo(int((wl-2000)/(11000.-2000.) * 256))

        if phase:
            xx = (tds.lc_data.mjd[idx] - tmax) / (1. + z)
            ax.axvline(0., ls=':')
            xmin.append(min(xx.min()-2, -10.))
            xmax.append(max(xx.max()+2, +40.))
        else:
            xx = tds.lc_data.mjd[idx]
            ax.axvline(tmax, ls=':')
            xmin.append(min(xx.min()-2, tmax-10.))
            xmax.append(max(xx.max()+2, tmax+40.))

        # we plot the calibrated fluxes. Therefore, we rescale them, using the
        # zero points reported with each flux measurement in the TrainingDataset
        if residuals:
            y = tds.lc_data.flux[idx] - model_val[idx]
            yerr = tds.lc_data.fluxerr[idx]
        elif pulls:
            y = tds.lc_data.flux[idx] - model_val[idx]
            sig2 = tds.lc_data.fluxerr[idx]**2
            if snake_val is not None:
                sig2 += snake_val[idx]
            y /= np.sqrt(sig2)
            yerr = np.zeros_like(y)
        else:
            y = tds.lc_data.flux[idx] * np.power(10, -0.4*tds.lc_data.zp[idx])
            yerr = tds.lc_data.fluxerr[idx] * np.power(10, -0.4*tds.lc_data.zp[idx])
            if static_snake is not None:
                static_snk = static_snake[:len(tds.lc_data.flux)]
                y_err_snk = static_snk[idx] * np.power(10, -0.4*tds.lc_data.zp[idx])

        ax.errorbar(xx, y, yerr=yerr, ls='', marker='o', color=color, label=b)
        if static_snake is not None:
            ax.fill_between(xx, y-y_err_snk, y+y_err_snk, color=color, alpha=0.2)
        if not(np.all(~np.isnan(y))):
            logging.warning(f'NaN detected in model: {tds.lc_data.flux[idx]} {tds.lc_data.zp[idx]}')
        if not(np.all(~np.isnan(yerr))):
            logging.warning(f'NaN detected in error model: {tds.lc_data.fluxerr[idx]} {tds.lc_data.zp[idx]}')

        ymin.append(min(0., (y-2*yerr).min()))
        ymax.append((y+2*yerr).max())

        if p:
            p.plot(b, ax=ax,
                   color=color,
                   phase=phase,
                   ylabel='flux')
            # ymin.append(p.ymin)
            ymax.append(p.ymax)

    ax.set_xlim(np.min(xmin), np.max(xmax))
    ax.set_ylim(np.min(ymin), np.max(ymax))
    if phase:
        ax.set_xlabel('phase [restframe days]')
    else:
        ax.set_xlabel('mjd [days]')

    text = f"""SN: {sn:>15}
z: {z:>15.3f}"""
    legend = ax.legend(loc='best', title=text)
    legend_bbox = legend.get_window_extent(renderer=fig.canvas.get_renderer())
    legend_coords = ax.transAxes.inverted().transform((legend_bbox.x0, legend_bbox.y0))

    if ax is None:
        fig.suptitle(f'{sn} @ z={z:4.3}')
    save_figure(fig, savefig, output_dir, 'sn_lightcurves', ext)


def plot_phot_training_residuals(model, pars, snake=None,
                                 title='',
                                 savefig=None,
                                 output_dir=None,
                                 ext='.png'):
    """Plot the photometric training residuals and pulls
    """
    tds = model.training_dataset

    n_phot, n_spec, n_spectrophot = tds.nb_meas(split_by_type=1)
    if n_phot < 0:
        return
    v = model(pars)

    fig, axes = plt.subplots(figsize=(12,12), nrows=2, ncols=2)
    fig.suptitle(title)
    x = np.arange(n_phot)
    fluxerr = tds.lc_data.fluxerr
    if snake is not None:
        snk = snake(pars)
        w = 1. / np.sqrt(fluxerr**2 + snk[:n_phot])
    else:
        w = 1. / fluxerr
    res = tds.lc_data.flux-v[:n_phot]
    wres = w * (tds.lc_data.flux-v[:n_phot])  # / tds.lc_data.fluxerr
    ii = np.argsort(tds.lc_data.z)
    ii = np.arange(len(tds.lc_data.z))
    axes[0,0].errorbar(x, res[ii], yerr=fluxerr[ii], ls='', marker=',', color='gray')
    axes[0,0].scatter(x, res[ii], c=tds.lc_data.z[ii], s=2, zorder=100, norm='log')
    axes[0,0].set_ylabel('residuals')

    axes[1,0].plot(x, wres[ii], ls='', marker=',', color='gray')
    axes[1,0].scatter(x, wres[ii], c=tds.lc_data.z[ii], s=2, zorder=100, norm='log')
    axes[1,0].set_xlabel('meas index')
    axes[1,0].set_ylabel('pulls')

    phase = (tds.lc_data.mjd - pars['tmax'].full[tds.lc_data.sn_index]) / (1. + tds.lc_data.z)
    axes[0,1].errorbar(phase[ii], res[ii], yerr=fluxerr[ii], ls='', color='gray', marker='.')
    axes[0,1].scatter(phase[ii], res[ii], c=tds.lc_data.z[ii], s=2, zorder=100, norm='log')
    axes[0,1].set_ylabel('residuals')

    axes[1,1].plot(phase[ii], wres[ii], ls='', color='gray', marker='.')
    axes[1,1].scatter(phase[ii], wres[ii], c=tds.lc_data.z[ii], s=2, zorder=100, norm='log')
    axes[1,1].set_xlabel('phase [days]')
    axes[1,1].set_ylabel('pulls')

    save_figure(fig, savefig, output_dir, 'phot_training_residuals', ext)

    return v, res, wres


def plot_phot_chi2_phasespace(model, pars, snake=None,
                              title='',
                              nwl=100, nph=100, vmin=0, vmax=16,
                              savefig=None,
                              output_dir=None,
                              ext='.png'):
    """plot the photometric residuals partial chi2 in the SN phase space
    """
    tds = model.training_dataset
    n_phot, n_spec, n_spectrophot = tds.nb_meas(split_by_type=1)
    if n_phot < 0:
        return

    v = model(pars)
    flux = tds.lc_data.flux
    fluxerr = tds.lc_data.fluxerr
    if snake is not None:
        snk = snake(pars)
        w = 1. / np.sqrt(fluxerr**2 + snk[:n_phot])
    else:
        w = 1. / fluxerr
    wres = w * (flux - v[:n_phot])
    zz = 1. + tds.lc_data.z
    wl = tds.lc_data.wavelength / zz
    phase = (tds.lc_data.mjd - pars['tmax'].full[tds.lc_data.sn_index]) / zz

    fig = plt.figure(figsize=(12,8))
    gs = gridspec.GridSpec(3, 2, width_ratios=[4,1])
    with np.errstate(divide='ignore', invalid='ignore'):
        hh, xx, yy = np.histogram2d(wl, phase, weights=wres**2, bins=(nwl,nph))
        norm, _, _ = np.histogram2d(wl, phase, bins=(nwl, nph))
        cell_chi2 = hh / norm
    ax = fig.add_subplot(gs[:,0])
    ax.set_xlabel(r'$\lambda$ [restframe, $\AA$]')
    ax.set_ylabel(r'phase [restframe, days]')
    im = ax.imshow(cell_chi2.T, vmin=vmin, vmax=vmax,
                   extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                   origin='lower',
                   aspect='auto')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.08)
    fig.colorbar(im, cax=cax, orientation='vertical')

    ax = fig.add_subplot(gs[0,1])
    ax.hist(wres, bins=100, density=True, log=True)
    ax.set_xlabel('wres')

    ax = fig.add_subplot(gs[1,1])
    ax.hist(phase, bins=100, density=True, log=True)
    ax.set_xlabel('phases')

    fig.suptitle(title)
    plt.subplots_adjust(hspace=0.25)

    save_figure(fig, savefig, output_dir, 'phot_chi2_phasespace', ext)


def plot_lc_partial_chi2(model, pars, snake=None, group_by='sn',
                         savefig=None,
                         output_dir=None,
                         ext='.png'):
    """Plot the partial chi2 of each light curve
    """
    tds = model.training_dataset

    n_phot, n_spec, n_spphot = tds.nb_meas(split_by_type=1)
    v = model(pars)
    res = tds.lc_data.flux - v[:n_phot]
    fluxerr = tds.lc_data.fluxerr
    if snake is not None:
        snk = snake(pars)
        w = 1. / np.sqrt(fluxerr**2 + snk[:n_phot])
    else:
        w = 1. / fluxerr
    wres = w * res

    if group_by is None or group_by == 'sn':
        xx_count = tds.lc_data.sn_index
        xx = np.arange(len(tds.sn_data.sn_set))
        zz = np.zeros(len(tds.sn_data.sn_set))
        zz[tds.sn_data.sn_index] = tds.sn_data.z
    elif group_by == 'lc':
        xx_count = tds.lc_data.lc_index
        xx = np.arange(len(tds.lc_data.lc_set))
        wl = np.zeros(len(tds.lc_data.lc_set))
        wl[tds.lc_data.lc_index] = tds.lc_data.wavelength

    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = np.bincount(xx_count, weights=wres**2)
        nn = np.bincount(xx_count)
        chi2nn = chi2 / nn

    fig, axes = plt.subplots(figsize=(12,12), nrows=2, ncols=1)
    if group_by == 'sn':
        axes[0].scatter(xx, chi2nn, c=zz)
        axes[0].set_xlabel(f'{group_by}_index')
        axes[0].set_ylabel(rf'$\chi^2_{group_by}$')
        axes[0].set_title(f'lightcurves: {group_by} chi2 vs. {group_by}_index')
    else:
        axes[0].scatter(xx, chi2nn, c=wl)
        axes[0].set_xlabel(f'{group_by}_index')
        axes[0].set_ylabel(rf'$\chi^2_{group_by}$')
        axes[0].set_title(f'lightcurves: {group_by} chi2 vs. {group_by}_index')

    if group_by == 'sn':
        axes[1].scatter(zz, chi2/nn, c=zz)
        axes[1].set_xlabel('z')
        axes[1].set_ylabel(rf'$\chi^2_{group_by}$')
        axes[1].set_title(f'lightcurves: {group_by} chi2 vs. z')
    if group_by == 'lc':
        axes[1].scatter(wl, chi2/nn, c=wl)
        axes[1].set_xlabel(r'$\lambda_{rest}$')
        axes[1].set_ylabel(rf'$\chi^2_{group_by}$')
        axes[1].set_title(f'lightcurves: {group_by} chi2 vs. restframe wavelength')

    axes[1].set_yscale('log')
    save_figure(fig, savefig, output_dir, 'lc_partial_chi2', ext)

    return chi2, nn

def plot_lc_pulls_per_band(tds, model, pars, snake=None,
                           savefig=None,
                           output_dir=None,
                           ext='.png'):
    def gaussian(x, A, x0):
        """
        1 gaussian with sigma=1
        """
        return A * np.exp(-(x-x0)**2)


    nb_bands = len(tds.lc_data.band_set)
    v = model(pars)
    if snake is not None:
        var = snake(pars)
    else:
        var = np.zeros(len(v))
    v_lc = v[:len(tds.lc_data)]
    var_lc = var[:len(tds.lc_data)]

    fig, axs = plt.subplots(nrows=nb_bands, ncols=2, gridspec_kw={'width_ratios': [3, 1]}, sharey='row', figsize=(14, 10))
    bands = np.unique(tds.lc_data.nt['band'])
    color = ['black', 'blue', 'brown', 'chocolate', 'darkblue',  'darkgreen', 'darkolivegreen', 'darkred', 'darkorange',
    'darkmagenta', 'darkviolet', 'green', 'olive', 'red', 'orange', 'magenta', 'gold',  'pink', 'teal']
    cc = np.random.choice(np.array(color), size=nb_bands, replace=False)

    for i in range(nb_bands):
        idx = tds.lc_data.band == bands[i]
        band_name = tds.lc_data.band[idx][0]

        res = (tds.lc_data.flux[idx] - v_lc[idx])/np.sqrt(tds.lc_data.fluxerr[idx]**2+var_lc[idx])
        p = tds.lc_data.mjd[idx] - pars['tmax'].full[tds.lc_data.sn_index][idx]
        
        hist = np.histogram(res, bins=100)
        popt, pcov = curve_fit(gaussian, (hist[1][:-1] + hist[1][1:])/2, hist[0])
        
        axs[i, 0].errorbar(p, res, yerr=tds.lc_data.fluxerr[idx]*0, fmt='.', label=band_name, color=cc[i])
        axs[i, 1].hist(res, bins=100, orientation='horizontal', color=cc[i])
        axs[i, 1].plot(gaussian((hist[1][:-1] + hist[1][1:])/2, *popt), (hist[1][:-1] + hist[1][1:])/2 , color='C0')
        axs[i, 1].set_ylim(np.mean(res) - 5 * np.std(res), np.mean(res) + 5 * np.std(res))

        axs[i, 0].set_ylabel('pulls')
        axs[i, 0].legend()

        # Remove the x-tick labels for all but the bottom row
        if i < nb_bands - 1:
            axs[i, 0].tick_params(labelbottom=False)
            axs[i, 1].tick_params(labelbottom=False)

    axs[nb_bands - 1, 0].set_xlabel('phase')

    # Adjust the layout
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.05)  # Adjust hspace to reduce the vertical spacing
    save_figure(fig, savefig, output_dir, 'lc_pulls_per_band', ext)

def plot_all_lightcurves(model, pars, snake=None):
    """
    """
    pass
