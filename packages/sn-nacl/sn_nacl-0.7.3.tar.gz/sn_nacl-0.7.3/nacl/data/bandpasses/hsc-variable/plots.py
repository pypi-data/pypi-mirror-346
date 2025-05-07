
import numpy as np
import pylab as pl
import sncosmo



filter_repo = '/home/nrl/salt3/naclprod/data/bandpasses/hsc-variable'


def register_bandpasses(filter_repo=filter_repo):
    """
    """
    for band in ['g', 'r', 'i', 'z', 'y', 'r2', 'i2']:
        b = sncosmo.snfitio.read_snfit_bandpass_interpolator(filter_repo, band, name=band)
        sncosmo.bandpasses._BANDPASS_INTERPOLATORS.register(b, 'hsc::' + band)
        # sncosmo.register(b, 'hsc::' + band)


def plot_transmissions(band, axes=None, title='', legend=False):
    """
    """
    if axes is None:
        fig, axes = pl.subplots(nrows=1, ncols=1, figsize=(10,10))

    nrads = 30
    dcol = int(256 / nrads)
    for i,rad in enumerate(np.linspace(0, 28-0.1, 30)):
        b = sncosmo.get_bandpass(band, rad)
        wl = np.linspace(b.minwave(), b.maxwave(), 250)
        axes.plot(wl, b(wl), ls='-', alpha=0.25, color=pl.cm.jet_r(i * dcol),
                  label=f'rad: {rad:.2f} cm')
    axes.set_xlabel(r'$\lambda [\AA]$') #  fontsize=18)
    axes.set_ylabel(r'$T(\lambda)$') # fontsize=18)
    fig = pl.gcf()
    fig.suptitle(title)
    if legend:
        pl.legend(loc='best')


def plot_wave_eff_vs_rad(band, axes=None, xlabel='', ylabel='', title='', ls='-', label='', legend=False):
    """
    """
    if axes is None:
        fig, axes = pl.subplots(nrows=1, ncols=1, figsize=(8,8))

    rads = np.arange(0., 28., 0.1)
    wave_eff = []
    for r in np.arange(0., 28, 0.1):
        tr = sncosmo.get_bandpass(band, r)
        wave_eff.append(tr.wave_eff)
    wave_eff = np.array(wave_eff)
    w = wave_eff[0]
    col = pl.cm.jet(int(256 * (w-4000)/(8500-3000)))

    axes.axhline(0, lw=1, color='gray')
    axes.axhspan(-0.001, 0.001, color='gray', alpha=0.1)

    axes.plot(rads, (wave_eff-wave_eff[0])/wave_eff[0], ls=ls, lw=2, color=col, label=label)
    if xlabel:
        axes.set_xlabel(xlabel)
    if ylabel:
        axes.set_ylabel(ylabel)
    pl.subplots_adjust(hspace=0.005, wspace=0.005)
    if title:
        axes.text(0.5, 0.9, f'{band}',
                  horizontalalignment='center',
                  verticalalignment='center',
                  transform = axes.transAxes)

    axes.set_ylim((-0.007, 0.007))
    if legend:
        axes.legend(loc='lower left')


def plot_throughput_vs_rad(band, axes=None, xlabel='', ylabel='', title='', ls='-', label='', legend=False):
    """
    """
    if axes is None:
        fig, axes = pl.subplots(nrows=1, ncols=1, figsize=(8,8))

    rads = np.arange(0., 27., 0.1)
    throughputs = []
    wave_eff = []
    for r in np.arange(0., 27, 0.1):
        tr = sncosmo.get_bandpass(band, r)
        wl = np.linspace(tr.minwave(), tr.maxwave(), 100)
        throughputs.append(tr(wl).sum())
        wave_eff.append(tr.wave_eff)
    throughputs = np.array(throughputs)

    col = pl.cm.jet(int(256 * (wave_eff[0]-4000)/(8500-3000)))
    axes.axhline(0, lw=1, color='gray')
    axes.axhspan(-0.01, 0.01, color='gray', alpha=0.1)

    axes.plot(rads, (throughputs-throughputs[0])/throughputs[0], ls=ls, lw=2, color=col, label=label)
    if xlabel:
        axes.set_xlabel(xlabel)
    if ylabel:
        axes.set_ylabel(ylabel)
    pl.subplots_adjust(hspace=0.005, wspace=0.005)
    if title:
        axes.text(0.5, 0.9, f'{band}',
                  horizontalalignment='center',
                  verticalalignment='center',
                  transform = axes.transAxes)

    axes.set_ylim((-0.1, 0.1))
    if legend:
        axes.legend(loc='lower left')


def all_plots():
    """
    """
    # all bands, r,i
    fig, axes = pl.subplots(nrows=1, ncols=1, figsize=(16,6))
    for b in ['hsc::'  + b for b in ['g', 'r', 'i', 'z', 'y']]:
        plot_transmissions(b, axes=axes, title='all bands, original r and i')

    # all bands, r2, i2
    fig, axes = pl.subplots(nrows=1, ncols=1, figsize=(16,8))
    for b in ['hsc::'  + b for b in ['g', 'r2', 'i2', 'z', 'y']]:
        plot_transmissions(b, axes=axes, title='all bands, new r2 and i2')

    # all bands, zoom
    for b in ['hsc::'  + b for b in ['g', 'r', 'r2', 'i', 'i2', 'z', 'y']]:
        plot_transmissions(b, title=b, legend=True)

    # mean wavelength versus r
    fig, axes = pl.subplots(nrows=2, ncols=3, figsize=(12,8), sharex=True, sharey=True)
    plot_wave_eff_vs_rad('hsc::g',  axes=axes[0,0], ylabel=r'$\delta\lambda/\lambda$', title='g')
    plot_wave_eff_vs_rad('hsc::r',  axes=axes[0,1], title='r', label='r', ls=':')
    plot_wave_eff_vs_rad('hsc::r2', axes=axes[0,1], label='r2', legend=1)
    plot_wave_eff_vs_rad('hsc::i',  axes=axes[0,2], title='i', label='i', ls=':')
    plot_wave_eff_vs_rad('hsc::i2', axes=axes[0,2], xlabel='rad [cm]', label='i2', legend=1)
    plot_wave_eff_vs_rad('hsc::z',  axes=axes[1,0], xlabel='rad [cm]', ylabel=r'$\delta\lambda/\lambda$', title='hsc::z')
    plot_wave_eff_vs_rad('hsc::y',  axes=axes[1,1], xlabel='rad [cm]', title='hsc::y')
    pl.setp(axes[1,2], visible=False)
    fig.suptitle(r'HSC filter uniformity ($\lambda$)')


    # mean wavelength versus r
    fig, axes = pl.subplots(nrows=2, ncols=3, figsize=(12,8), sharex=True, sharey=True)
    plot_throughput_vs_rad('hsc::g',  axes=axes[0,0], ylabel=r'$\delta \int T/ \int T$', title='g')
    plot_throughput_vs_rad('hsc::r',  axes=axes[0,1], title='r', label='r', ls=':')
    plot_throughput_vs_rad('hsc::r2', axes=axes[0,1], label='r2', legend=1)
    plot_throughput_vs_rad('hsc::i',  axes=axes[0,2], title='i', label='i', ls=':')
    plot_throughput_vs_rad('hsc::i2', axes=axes[0,2], xlabel='rad [cm]', label='i2', legend=1)
    plot_throughput_vs_rad('hsc::z',  axes=axes[1,0], xlabel='rad [cm]', ylabel=r'$\delta\int T/\int T$', title='hsc::z')
    plot_throughput_vs_rad('hsc::y',  axes=axes[1,1], xlabel='rad [cm]', title='hsc::y')
    pl.setp(axes[1,2], visible=False)
    fig.suptitle(r'HSC filter uniformity ($\int T$)')


    return axes



    # throughput versus r
