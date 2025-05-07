
import numpy as np
import pylab as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from ..plotting import save_figure


def plot_gamma_sn_like_error_snake(snake, pars, savefig=None,
                                   output_dir=None,
                                   ext='.png'):
    """
    """
    tds = snake.training_dataset

    fig, axes = plt.subplots(figsize=(12,12), nrows=2, ncols=2)
    fig.suptitle('Error Snake')
    axes[0,0].scatter(tds.sn_data.nt['x1'],
                      pars['gamma_sn'].full[tds.sn_data.sn_index]**2,
                      c=tds.sn_data.z, s=5)
    axes[0,0].set_xlabel('$x_1$')
    axes[0,0].set_ylabel(r'$\gamma_{SN}$')

    axes[0,1].scatter(tds.sn_data.nt['c'],
                      pars['gamma_sn'].full[tds.sn_data.sn_index]**2,
                      c=tds.sn_data.z, s=5)
    axes[0,1].set_xlabel('$c$')

    # axes[1,0].scatter(tds.sn_data.nt['tmax'],
    #                   pars['gamma_sn'].full[tds.sn_data.sn_index]**2,
    #                   c=tds.sn_data.z, s=5)
    # axes[1,0].set_xlabel('$t_{\\mathrm{max}}$')
    # axes[1,0].set_ylabel('$\\gamma_{SN}$')

    axes[1,0].scatter(tds.sn_data.z[tds.sn_data.sn_index],
                      pars['gamma_sn'].full[tds.sn_data.sn_index]**2,
                      c=tds.sn_data.z, s=5)
    axes[1,0].set_xlabel('$z$')
    axes[1,0].set_ylabel('$\\gamma_{SN}$')

    xx = np.linspace(snake.basis.bx.grid.min(), snake.basis.bx.grid.max(), 100)
    yy = np.linspace(snake.basis.by.grid.min(), snake.basis.by.grid.max(), 100)
    X, Y = np.meshgrid(xx, yy)
    J = snake.basis.eval(X.flatten(), Y.flatten())
    im = axes[1,1].imshow((J @ pars['gamma_snake'].full).reshape(100,100),
                          aspect='auto',
                          origin='lower',
                          extent=(xx.min(), xx.max(), yy.min(), yy.max())
                          )
    axes[1,1].set_xlabel(r'wavelength [$\AA$, resframe]')
    axes[1,1].set_ylabel('phase [days, restframe]')
    divider = make_axes_locatable(axes[1,1])
    cax = divider.append_axes('right', size='5%', pad=0.08)
    fig.colorbar(im, cax=cax, orientation='vertical')

    save_figure(fig, savefig, output_dir, 'gamma_sn_like_error_snake', ext)
