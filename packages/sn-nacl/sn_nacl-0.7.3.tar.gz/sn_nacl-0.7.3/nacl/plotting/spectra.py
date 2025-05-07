"""spectrum plotting routines
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from ..plotting import save_figure


def _get_axis(axes, sn, col, nrows, ncols):
    if ncols > 1 and nrows > 1:
        return axes[sn,col]
    elif ncols == 1 and nrows > 1:
        return axes[sn]
    elif ncols > 1 and nrows == 1:
        return axes[col]
    return axes


def plot_sn_spectra(model, pars,
                    sn_index=None, sn=None,
                    snake=None,
                    alpha=0.25,
                    plot_pulls=False,
                    plot_residuals=False,
                    savefig=None,
                    output_dir=None,
                    ext='.png'):
    """
    """
    tds = model.training_dataset

    sel = None
    if sn is not None:
        sel = tds.spec_data.sn == sn
        sn_index = tds.sn_data.sn_map[sn]
    elif sn_index is not None:
        sel = tds.spec_data.sn_index == sn_index
        sn = tds.sn_data.sn_set[sn_index]

    n_phot, n_spec, n_spphot = tds.nb_meas(split_by_type=1)
    spectra = np.unique(tds.spec_data.spec[sel]).tolist()
    nrows = len(spectra)
    v = model(pars)
    snk = snake(pars) if snake is not None else None

    ncols = 1
    if plot_residuals:
        ncols += 1
    if plot_pulls:
        ncols += 1
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols,
                             figsize=(8,12),
                             sharex=True)

    for i,s in enumerate(spectra):
        col = 0
        # plot the main spectrum
        idx = sel & (tds.spec_data.spec == s)
        # ax = axes[i] if nrows > 1 else axes
        ax = _get_axis(axes, i, col, nrows, ncols)
        ax.errorbar(tds.spec_data.wavelength[idx],
                    tds.spec_data.flux[idx],
                    yerr=tds.spec_data.fluxerr[idx],
                    ls='', marker='.', color='blue')


        vv = v[n_phot:][idx]
        ax.plot(tds.spec_data.wavelength[idx], vv, 'r+:')
        if snk is not None:
            vv_var = snk[len(tds.lc_data):][idx]
            vmin = vv - np.sqrt(vv_var)
            vmax = vv + np.sqrt(vv_var)
            ax.fill_between(tds.spec_data.wavelength[sel],
                            vmin, vmax,
                            color='r', alpha=alpha)
        else:
            vv_var = np.zeros(len(vv))

        ax.set_ylabel('flux')
        ax.set_xlabel('mjd')

        if plot_residuals:
            col += 1
            ax = _get_axis(axes, i, col, nrows, ncols)
            ax.errorbar(tds.spec_data.wavelength[idx],
                        vv-tds.spec_data.flux[idx],
                        yerr=tds.spec_data.fluxerr[idx],
                        ls='', marker='.', color='blue')
            if i == 0:
                ax.set_title('residuals')

        if plot_pulls:
            col += 1
            ax = _get_axis(axes, i, col, nrows, ncols)
            ax.plot(tds.spec_data.wavelength[idx],
                    (vv-tds.spec_data.flux[idx]) / np.sqrt(vv_var + tds.spec_data.fluxerr[idx]**2),
                    ls='', marker='.', color='blue')
            if i == 0:
                ax.set_title('pulls')

        sn = np.unique(tds.spec_data.sn[idx])
        assert len(sn) == 1
        sn = sn[0]
        z = np.unique(tds.spec_data.z[idx])
        assert len(z) == 1
        z = z[0]
        fig.suptitle(f'{sn} @ z={z:4.3}')
        plt.subplots_adjust(hspace=0.05)

        save_figure(fig, savefig, output_dir, f'sn_spectra_{sn}', ext)


def plot_spectrum(model, pars,
                  spec_index,
                  snake=None,
                  alpha=0.25,
                  pulls=False,
                  residuals=False,
                  ax=None,
                  savefig=None,
                  output_dir=None,
                  ext='.png'):
    """
    """
    tds = model.training_dataset

    sel = tds.spec_data.spec_index == spec_index
    sn = np.unique(tds.spec_data.sn[sel])
    assert sn.size == 1, f"No unique sn value found: {sn}"
    sn = sn.item()

    sn_idx = tds.sn_data.sn == sn
    z = float(tds.sn_data.z[sn_idx])
    label = f'{sn} @ z={z:4.3}'

    n_phot, n_spec, n_spphot = tds.nb_meas(split_by_type=1)
    v = model(pars)
    v_spec = v[n_phot:]
    if snake is not None:
        snk = snake(pars)
        snk_spec = snk[n_phot:]
    else:
        snk_spec = np.zeros_like(v_spec)

    # plots
    if ax is None:
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()

    # let's plot the spectrum now
    x = tds.spec_data.wavelength[sel]
    if residuals:
        y = tds.spec_data.flux[sel] - v_spec[sel]
        yerr = np.sqrt(tds.spec_data.fluxerr[sel]**2 + snk_spec[sel])
    elif pulls:
        y = tds.spec_data.flux[sel] - v_spec[sel]
        sig = np.sqrt(tds.spec_data.fluxerr[sel]**2 + snk_spec[sel])
        y /= sig
        yerr = np.zeros_like(len(y))
    else:
        y = tds.spec_data.flux[sel]
        # we only plot the measurement uncertainties,
        # the error snake is plot along with the model
        yerr = tds.spec_data.fluxerr[sel]

    ax.errorbar(x, y, yerr=yerr, ls='', marker='.', label=label)
    ax.plot(tds.spec_data.wavelength[sel], v_spec[sel], 'r+:')
    if snk_spec is not None:
        vmin = v_spec[sel] - np.sqrt(snk_spec[sel])
        vmax = v_spec[sel] + np.sqrt(snk_spec[sel])
        ax.fill_between(x, vmin, vmax, color='r', alpha=alpha)

    ax.legend(loc='best')
    plt.subplots_adjust(hspace=0.05)

    save_figure(fig, savefig, output_dir, f'spectrum_{spec_index}', ext)


def plot_spec_training_residuals(model, pars, snake=None, title='',
                                 savefig=None,
                                 output_dir=None,
                                 ext='.png'):
    """Plot the spectroscopic training residuals
    """
    tds = model.training_dataset

    n_phot, n_spec, n_spectrophot = tds.nb_meas(split_by_type=1)
    if n_phot < 0:
        return
    v = model(pars)

    x = np.arange(n_spec)
    flux = tds.spec_data.flux
    fluxerr = tds.spec_data.fluxerr
    if snake is not None:
        snk = snake(pars)[n_phot:]
        w = 1. / np.sqrt(fluxerr**2 + snk)
    else:
        w = 1. / fluxerr
    res = tds.spec_data.flux-v[n_phot:]
    wres = w * (tds.spec_data.flux-v[n_phot:]) # / tds.spec_data.fluxerr

    fig, axes = plt.subplots(figsize=(12,12), nrows=2, ncols=2)
    fig.suptitle(title)
    axes[0,0].errorbar(x, res, yerr=fluxerr, ls='', marker=',', color='gray')
    axes[0,0].scatter(x, res, c=tds.spec_data.z, s=2, zorder=100, norm='log')
    axes[0,0].set_ylabel('residuals')

    axes[1,0].plot(x, wres, ls='', marker=',', color='gray')
    axes[1,0].scatter(x, wres, c=tds.spec_data.z, s=2, zorder=100, norm='log')
    axes[1,0].set_xlabel('meas index')
    axes[1,0].set_ylabel('pulls')

    # phase = (tds.spec_data.mjd - pars['tmax'].full[tds.spec_data.sn_index]) / (1. + tds.spec_data.z)
    wl = tds.spec_data.wavelength / (1. + tds.spec_data.z)
    axes[0,1].errorbar(wl, res, yerr=fluxerr, ls='', color='gray', marker='.')
    axes[0,1].scatter(wl, res, c=tds.spec_data.z, s=2, zorder=100, norm='log')
    axes[0,1].set_ylabel('residuals')

    axes[1,1].plot(wl, wres, ls='', color='gray', marker='.')
    axes[1,1].scatter(wl, wres, c=tds.spec_data.z, s=2, zorder=100, norm='log')
    axes[1,1].set_xlabel(r'restframe wavelength ($\AA$)')
    axes[1,1].set_ylabel('pulls')

    save_figure(fig, savefig, output_dir, 'spec_training_residuals', ext)

    return v, res, wres


def plot_spec_chi2_phasespace(model, pars, snake=None,
                              title='',
                              nwl=100, nph=100, vmin=0., vmax=16,
                              savefig=None,
                              output_dir=None,
                              ext='.png'):
    """
    """
    tds = model.training_dataset
    n_phot, n_spec, n_spectrophot = tds.nb_meas(split_by_type=1)
    if n_spec < 0:
        return

    v = model(pars)
    flux = tds.spec_data.flux
    fluxerr = tds.spec_data.fluxerr
    if snake is not None:
        snk = snake(pars)
        w = 1. / np.sqrt(fluxerr**2 + snk[n_phot:])
    else:
        w = 1. / fluxerr
    zz = 1. + tds.spec_data.z
    wl = tds.spec_data.wavelength / zz
    phase = (tds.spec_data.mjd - pars['tmax'].full[tds.spec_data.sn_index]) / zz
    if snake is not None:
        snk = snake(pars)
        w = 1. / np.sqrt(fluxerr**2 + snk[n_phot:])
    else:
        w = 1. / fluxerr
    wres = w * (flux - v[n_phot:])

    with np.errstate(divide='ignore', invalid='ignore'):
        hh, xx, yy = np.histogram2d(wl, phase, weights=wres**2, bins=(nwl,nph))
        norm, _, _ = np.histogram2d(wl, phase, bins=(nwl,nph))
        cell_chi2 = hh / norm

    fig = plt.figure(figsize=(12,8))
    gs = gridspec.GridSpec(3, 2, width_ratios=[4,1])
    ax = fig.add_subplot(gs[:,0])
    ax.set_xlabel(r'$\lambda$ [restframe, $\AA$]')
    ax.set_ylabel('phase [restframe, days]')
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
    ax.set_xlabel('phase')

    fig.suptitle(title)
    plt.subplots_adjust(hspace=0.25)

    save_figure(fig, savefig, output_dir, 'spec_chi2_phasespace', ext)


def plot_spec_partial_chi2(model, pars, snake=None, group_by='sn',
                           savefig=None,
                           output_dir=None,
                           ext='.png'):
    """
    """
    tds = model.training_dataset

    n_phot, n_spec, n_spphot = tds.nb_meas(split_by_type=1)
    v = model(pars)
    res = tds.spec_data.flux - v[n_phot:]
    fluxerr = tds.spec_data.fluxerr
    if snake is not None:
        snk = snake(pars)
        w = 1. / np.sqrt(fluxerr**2 + snk[n_phot:])
    else:
        w = 1. / fluxerr
    wres = w * res

    if group_by is None or group_by == 'sn':
        xx_count = tds.spec_data.sn_index
        nsn = len(tds.sn_data.sn_set)
        xx = np.arange(nsn)
        zz = np.zeros(nsn)
        zz[tds.sn_data.sn_index] = tds.sn_data.z
    elif group_by == 'spec':
        xx_count = tds.spec_data.spec_index
        nspec = len(tds.spec_data.spec_set)
        xx = np.arange(nspec)
        zz = np.zeros(nspec)
        zz[tds.spec_data.spec_index] = tds.spec_data.z

    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = np.bincount(xx_count, weights=wres**2, minlength=len(zz))
        nn = np.bincount(xx_count, minlength=len(zz))
        rchi2 = chi2 / nn

    fig, axes = plt.subplots(figsize=(12,12), nrows=2, ncols=1)
    axes[0].set_title(rf'spectrum partial $\chi^2$ vs. {group_by}_index')
    axes[0].scatter(xx, rchi2, c=zz)
    axes[0].set_xlabel(f'{group_by}_index')
    axes[0].set_ylabel(rf'$\chi^2_{group_by}$')

    axes[1].set_title(rf'spectrum partial $\chi^2$ vs. z')
    axes[1].scatter(zz, rchi2, c=zz)
    axes[1].set_xlabel('$z$')
    axes[1].set_ylabel(rf'$\chi^2_{group_by}$')

    # plt.scatter(np.arange(len(tds.sn_data)), chi2/nn, c=tds.sn_data.z[tds.sn_data.sn_index])

    save_figure(fig, savefig, output_dir, 'spec_partial_chi2', ext)

    return rchi2
