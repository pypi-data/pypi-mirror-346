import numpy as np
from scipy.sparse import dia_matrix
from sksparse import cholmod
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas
from bbf.bspline import BSpline


def gaussian(x, a, sigma):
    """
    Gaussian function *2
    """
    norm = a / (np.sqrt(2. * np.pi) * sigma)
    xx = x / sigma
    return norm * np.exp(-0.5 * xx**2)


class ToyDataGenerator:

    def __init__(self, xmin=-10., xmax=10., yerr=0.01, a=1., sigma=3.,
                 n=100, delta=2., bsize=10, order=4, error_pedestal=0.025):
        self.xmin, self.xmax = xmin, xmax
        self.yerr = yerr
        self.error_pedestal = error_pedestal
        if self.error_pedestal is not None:
            self.sig_noise = np.sqrt(self.yerr**2 + self.error_pedestal**2)
        else:
            self.sig_noise = yerr
        self.a, self.sigma = a, sigma
        self.n = n
        self.delta = delta
        self.basis = BSpline(np.linspace(xmin-delta, xmax+delta, bsize),
                             order=order)
        self.error_pedestal = error_pedestal

    def generate(self):
        """
        generate a realization of a dataset
        """
        x = np.random.uniform(self.xmin, self.xmax, size=self.n)
        y = gaussian(x, self.a, self.sigma)
        yerr = np.full(self.n, self.yerr)
        sig_noise = np.full(self.n, self.sig_noise)
        noise = np.random.normal(loc=0., scale=sig_noise)
        self.x, self.y_true, self.yerr, self.noise = x, y, yerr, noise
        self.y = self.y_true + self.noise
        return self.x, self.y + self.noise, self.yerr

    def get_data(self):
        if not hasattr(self, 'x'):
            self.generate()
        dd = pandas.DataFrame({'xx': self.x,
                               'y': self.y,
                               'yerr': self.yerr,
                               'bads': np.zeros(len(self.yerr)).astype(bool),
                               })
        return dd

    def fit(self, beta=1.E-6):
        """a fit of the data -- the simplest possible
        """
        J = self.basis.eval(self.x)
        w = 1. / self.yerr**2
        W = dia_matrix((w, [0]), shape=(self.n, self.n))
        H = J.T @ W @ J
        B = J.T @ W @ self.y
        fact = cholmod.cholesky(H, beta=beta)
        self.theta = fact(B)

    def plot(self, color='b', marker='.'):
        """plot the data and the model
        """
        fig = plt.figure()
        gs = GridSpec(2, 1, height_ratios=[4,2])

        ax1 = fig.add_subplot(gs[0])
        ax1.errorbar(self.x, self.y, yerr=self.yerr, ls='', color=color, marker=marker, label='data', zorder=0.5)
        ax1.set_ylabel(r'model \& data')
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        ax2.set_xlabel('x')
        ax2.set_ylabel('residuals')

        # pl.grid(ls=':')
        # pl.plot(self.basis.grid, np.zeros(len(self.basis.grid)), 'k|')
        if hasattr(self, 'theta'):
            xx = self.basis._grid.copy()
            JJ = self.basis.eval(xx)
            ax1.plot(xx, JJ@self.theta, ls='', color='red', marker='.', alpha=1., label='nodes', zorder=10., linewidth=2)

            xx = np.linspace(self.xmin-self.delta, self.xmax+self.delta, 200)
            JJ = self.basis.eval(xx)
            ax1.plot(xx, JJ@self.theta, 'r-', label='model', zorder=2.)

            JJ = self.basis.eval(self.x)
            ax2.errorbar(self.x, self.y-JJ @ self.theta, yerr=self.yerr, ls='', marker='.', color='k')

        plt.legend(loc='best')



def plot_model_and_data(model, pars, data, title='', reg_lambda=None):
    """
    """
    fig = plt.figure()
    gs = GridSpec(3, 1, height_ratios=[4,2,2])

    ax1 = fig.add_subplot(gs[0])
    ax1.errorbar(data.xx, data.y, yerr=data.yerr, ls='', marker='.')
    xx = np.linspace(model.basis.grid.min(), model.basis.grid.max(), 200)
    J = model.basis.eval(xx)
    ax1.plot(xx, J @ pars['theta'].full, 'r-', zorder=10)
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax1.set_ylabel(r'model \& data')
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    res = data.y-model(pars)
    ax2.errorbar(data.xx, res, yerr=data.yerr, ls='', marker='.')
    ax2.set_xlabel('x')
    ax2.set_ylabel('residuals')
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    pars = pars.copy()
    xx = np.linspace(model.basis.grid.min(), model.basis.grid.max(), 500)
    J = model.basis.eval(xx)
    for i in range(len(pars['theta'].full)):
        pars['theta'].full[:] = 0.
        pars['theta'].full[i] = 3 * res.std()
        if reg_lambda is not None:
            color = plt.cm.jet(int(reg_lambda[i]/reg_lambda.max() * 256))
            # color = 'r' if reg_lambda[i]>0. else 'b'
        else:
            color = plt.cm.jet(int(i * 256/len(pars['theta'].full)))
        ax3.plot(xx, J@pars['theta'].full, ls='-', color=color)
    ax3.set_xlabel('x')

    plt.subplots_adjust(hspace=0.05)
    fig.suptitle(title)
