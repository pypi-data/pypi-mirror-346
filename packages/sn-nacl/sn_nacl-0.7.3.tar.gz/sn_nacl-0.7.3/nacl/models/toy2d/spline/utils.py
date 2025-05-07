import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import cm
import pandas

from bbf.bspline import BSpline
from bbf import bspline


def gaussian_2d(x, y, a, sigma):
    """
    Gaussian function *2
    """
    norm = a / (np.sqrt(2. * np.pi) * sigma)
    xx = x / sigma
    yy = y / sigma
    return norm * np.exp(-0.5 * (xx**2 + yy**2))

class ToyDataGenerator:

    def __init__(self, x0_min=-10., x0_max=10., x1_min=-10., x1_max=10., yerr=0.01, a=1., sigma=3.,
                 n0=40, n1=40, delta=2., b0_size=10, b1_size=10, order=4, error_pedestal=0.025):
        self.x0_min, self.x0_max = x0_min, x0_max
        self.x1_min, self.x1_max = x1_min, x1_max
        self.yerr = yerr
        self.error_pedestal = error_pedestal
        if self.error_pedestal is not None:
            self.sig_noise = np.sqrt(self.yerr**2 + self.error_pedestal**2)
        else:
            self.sig_noise = yerr
        self.a, self.sigma = a, sigma
        self.n0 = n0
        self.n1 = n1
        self.delta = delta
        self.basis = bspline.BSpline2D(np.linspace(x0_min-delta, x0_max+delta, b0_size), 
                                       np.linspace(x1_min-delta, x1_max+delta, b1_size), 
                                       x_order=order, y_order=order)
        #self.error_pedestal=error_pedestal

    def generate(self):
        """
        generate a realization of a dataset
        """
        x0 = np.random.uniform(self.x0_min, self.x0_max, size=self.n0)
        x1 = np.random.uniform(self.x1_min, self.x1_max, size=self.n1)
        X0, X1 = np.meshgrid(x0, x1)
        X0 = X0.ravel()
        X1 = X1.ravel()
        n = len(X0)
        self.n = n
        yerr = np.full(self.n, self.yerr)
        sig_noise = np.full(self.n, self.sig_noise)
        y = gaussian_2d(X0, X1, self.a, self.sigma)
        noise = np.random.uniform(low = -self.yerr, high = self.yerr, size = n)
        self.x0, self.x1, self.y_true, self.noise, self.yerr = x0, x1, y, noise, yerr
        self.y = self.y_true + self.noise
        return self.x0, self.x1, self.y + self.noise, self.yerr

    def get_data(self):
        if not hasattr(self, 'x0'):
            self.generate()
        X0, X1 = np.meshgrid(self.x0, self.x1)
        dd = pandas.DataFrame({'xx0': X0.ravel(),
                               'xx1': X1.ravel(),
                               'y': self.y,
                               'yerr': self.yerr,
                               'bads': np.zeros(len(self.yerr)).astype(bool),
                               })
        return dd

    #def fit(self, beta=1.E-6):
    #    """a fit of the data -- the simplest possible
    #    """
    #    X0, X1 = np.meshgrid(self.x0, self.x1)
    #    J = self.basis.eval(X0.ravel(), X1.ravel())
    #    w = 1. / self.yerr**2
    #    W = dia_matrix((w, [0]), shape=(self.n, self.n))
    #    H = J.T @ W @ J
    #    B = J.T @ W @ self.y
    #    fact = cholmod.cholesky(H, beta=1.E-6)
    #    self.theta = fact(B)

    def plot(self, color='b', marker='.'):
        """plot the data and the model
        """
        mu = self.mu
        fig = pl.figure()
        gs = GridSpec(2, 1, height_ratios=[7,2])

        ax1 = fig.add_subplot(gs[0], projection='3d')
        #ax1.errorbar(self.x, self.y, yerr=self.yerr, ls='', color=color, marker=marker, label='data', zorder=0.5)
        ax1.set_zlabel('model & data')
        ax1.set_xlabel('x0')
        ax1.set_ylabel('x1')
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        ax2.set_xlabel('x')
        ax2.set_ylabel('residuals')
        
        X0, X1 = np.meshgrid(self.x0, self.x1)
        ax1.errorbar(X0.ravel(), X1.ravel(), self.y, zerr = self.yerr, ecolor=('black',0.1), ls='', marker='.', color='blue')
        if self.mu ==0.:
            ax1.set_title('µ0 = ' +  str(self.mu_0) + ' , µ1 = ' + str(self.mu_1))
        else : 
            ax1.set_title('µ max = ' + str(self.mu))
            

        # pl.grid(ls=':')
        # pl.plot(self.basis.grid, np.zeros(len(self.basis.grid)), 'k|')
        
        resid = []
        errs = []
        if hasattr(self, 'theta'):
            #xx = self.basis._grid.copy()
            xx = self.basis.bx.grid
            yy = self.basis.by.grid
            XX, YY = np.meshgrid(xx, yy)
            JJ = self.basis.eval(XX.ravel(), YY.ravel())
            #ax1.plot(xx, yy, JJ@self.theta, ls='', color='red', marker='.', alpha=1., label='nodes', zorder=10., linewidth=2)
            fitting = JJ@self.theta
            fitting = np.reshape(fitting, (self.b0, self.b1))
            ax1.plot_surface(XX, YY, fitting, cmap=cm.coolwarm, label='nodes')

            #xx = np.linspace(self.x0_min-self.delta, self.x0_max+self.delta, 200)
            #JJ = self.basis.eval(xx)
            #ax1.plot(xx, JJ@self.theta, 'r-', label='model', zorder=2.)

            JJ = self.basis.eval(X0.ravel(), X1.ravel())
            x = np.linspace(self.x0_min, self.x0_max, len(X0.ravel()))
            ax2.errorbar(x, self.y-JJ @ self.theta, yerr=self.yerr, ls='', marker='.', color='k')
            
            residuals_data = self.y-JJ @ self.theta
            pl.figure()
            pl.hexbin(X0.ravel(), X1.ravel(), residuals_data/self.yerr, gridsize=15)
            pl.colorbar()
            pl.title('Weighted Residuals')
            
        pl.legend(loc='best')

def plot_model_and_data(model, pars, data, title='', reg_lambda=None):
    """
    """
    fig = plt.figure()
    #gs = GridSpec(3, 1, height_ratios=[4,2,2])
    gs = GridSpec(2, 1, height_ratios=[7,2])
    ax1 = fig.add_subplot(gs[0], projection='3d')
        
    xx0 = np.linspace(model.basis.bx.grid.min(), model.basis.bx.grid.max(), 200)
    xx1 = np.linspace(model.basis.by.grid.min(), model.basis.by.grid.max(), 200)    
    XX0, XX1 = np.meshgrid(xx0, xx1)    
    J = model.basis.eval(XX0.ravel(), XX1.ravel())    
    YY = J@pars['theta'].full
    YY = np.reshape(YY, (200, 200))
    ax1.plot_surface(XX0, XX1, YY, cmap=cm.coolwarm)  
    
    ax1.errorbar(data.xx0, data.xx1, data.y, zerr=data.yerr, ecolor=('black',0.1), ls='', marker='.', color='blue')  
    #plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.set_zlabel('model and data')
    
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    res = data.y-model(pars)
    ax2.errorbar(data.xx0, res, yerr=data.yerr, ls='', marker='.')
    ax2.set_xlabel('x')
    ax2.set_ylabel('residuals')
    #plt.setp(ax2.get_xticklabels(), visible=False)

    #ax3 = fig.add_subplot(gs[2], sharex=ax1)
    #pars = pars.copy()
    #xx = np.linspace(model.basis.grid.min(), model.basis.grid.max(), 500)
    #J = model.basis.eval(xx)
    #for i in range(len(pars['theta'].full)):
    #    pars['theta'].full[:] = 0.
    #    pars['theta'].full[i] = 3 * res.std()
    #    if reg_lambda is not None:
    #        color = plt.cm.jet(int(reg_lambda[i]/reg_lambda.max() * 256))
    #        # color = 'r' if reg_lambda[i]>0. else 'b'
    #    else:
    #        color = plt.cm.jet(int(i * 256/len(pars['theta'].full)))
    #    ax3.plot(xx, J@pars['theta'].full, ls='-', color=color)
    #ax3.set_xlabel('x')

    #plt.subplots_adjust(hspace=0.05)
    #fig.suptitle(title)
