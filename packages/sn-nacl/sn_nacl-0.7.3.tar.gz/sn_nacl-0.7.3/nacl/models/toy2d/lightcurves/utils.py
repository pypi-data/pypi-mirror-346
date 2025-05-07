"""
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas
from saltworks import DataProxy
from bbf.bspline import BSpline
from .model import Model




def gaussian_2d(x, y, sigma):
    """
    Gaussian function *2
    """
    #norm = a / (np.sqrt(2. * np.pi) * sigma)
    xx = x / sigma
    yy = y / sigma
    return np.exp(-0.5 * (xx**2 + yy**2))


class ToyModelGenerator:

    def __init__(self, nsn=100, npts1=10, npts2=10, nbands=1,
                 x1_min=-10., x1_max=10., x2_min=-10., x2_max=10., delta=10.,
                 yerr=0.01, error_pedestal=None, error_snake=None, wl_pivot=5000.):
        """
        .. note::
           error snake and error_pedestal are mutually exclusive.
           if error_snake > 0, then error_pedestal is set to zero
        """
        self.nsn = nsn
        self.npts1 = npts1
        self.npts2 = npts2
        self.nbands = nbands
        self.x1_min = x1_min
        self.x1_max = x1_max
        self.x2_min = x2_min
        self.x2_max = x2_max
        self.delta = delta
        self.yerr = yerr
        self.error_pedestal = 0.
        self.error_snake = 0.
        if error_pedestal is not None:
            self.error_pedestal = error_pedestal
        if error_snake is not None:
            self.error_pedestal = 0.
            self.error_snake = error_snake
        self.wl_pivot = wl_pivot

        self.sn_pars = {'x0_range': (0.1, 100.), 'tmax_margin': 5., 'stretch_range': (0., 0.25), 'color_pars': (0., 0.1)}
        self.lcpars = {'g': (0., 0.8), 'r': (0.2, 1.2), 'i': (0.7, 2.)}

    def gen_sample(self):
        """
        """
        # values and errors
        if 'x0_range' in self.sn_pars:
            xmin, xmax = self.sn_pars['x0_range']
            x0 = np.random.uniform(xmin, xmax, size=self.nsn)
        else:
            x0 = np.full(self.nsn, 1.)
        if 'tmax_margin' in self.sn_pars:
            tmax = np.random.uniform(self.x1_min+5, self.x1_max-5, size=self.nsn)
        else:
            tmax = np.full(self.nsn, 0.)
        if 'stretch_range' in self.sn_pars:
            stretch = np.random.normal(0., 0.25, size=self.nsn)
        else:
            stretch = np.full(self.nsn, 0.)

        if 'color_pars' in self.sn_pars:
            loc, sig = self.sn_pars['color_pars']
            color = np.random.normal(loc=loc, scale=sig, size=self.nsn)

        sample = pandas.DataFrame({'x0': x0, 'tmax': tmax, 'stretch': stretch, 'color': color})
        return sample

    def gen_data(self, sample):
        """
        """
        # generate the data structure
        npts = self.nsn * self.nbands * self.npts1 * self.npts2
        zz = np.random.uniform(1.0, 1.1, self.nsn)
        d = {
            'x1': np.random.uniform(self.x1_min, self.x1_max, npts),
            'x2': np.random.uniform(self.x2_min, self.x2_max, npts),
            'sn': np.repeat(np.arange(self.nsn), self.nbands * self.npts1 * self.npts2),
            'band': np.tile(np.repeat(np.arange(self.nbands), self.npts1 * self.npts2), self.nsn),
            'y': np.zeros(npts),
            'yerr': np.zeros(npts),
            'zz': np.repeat(zz, self.nbands * self.npts1 * self.npts2)
        }

        for band in self.lcpars:
            d['wl'] = 1500. * d['band'] + 4000.
            dwl = (d['wl'] - self.wl_pivot) / self.wl_pivot
            cl = 1. + dwl * sample.color[d['sn']]
            dt, sigma = self.lcpars[band]
            ph1 = (d['x1']-sample.tmax[d['sn']]-dt) * (1. + sample.stretch[d['sn']]) / d['zz'][d['sn']]
            ph2 = (d['x2']-sample.tmax[d['sn']]-dt) * (1. + sample.stretch[d['sn']]) / d['zz'][d['sn']]
            d['y'] = sample.x0[d['sn']] * gaussian_2d(ph1, ph2, sigma) / d['zz'][d['sn']]
            d['yerr'] = sample.x0[d['sn']] * np.full(npts, self.yerr)
            d['var'] = np.sqrt(self.error_pedestal**2 + self.error_snake**2 * d['y']**2)
        d = pandas.DataFrame(d)

        # add noise
        sig = np.sqrt(d.yerr**2 + self.error_pedestal**2 + self.error_snake**2 * d['y']**2)
        d['noise'] = np.random.normal(scale=sig, size=len(sig))
        d.y += d['noise']

        dp = DataProxy(d, x1='x1', x2='x2', sn='sn', band='band', wl='wl', y='y', yerr='yerr', var='var', zz='zz')
        dp.add_field('bads', np.zeros(len(dp.nt)).astype(bool))
        dp.make_index('sn')
        dp.make_index('band')

        return dp

    def gen_fine_grid(self, npts_per_lc=100):
        """
        """
        npts = 1 * self.nbands * npts_per_lc
        d = {
            'x1': np.tile(np.linspace(self.x1_min, self.x1_max, npts_per_lc), self.nbands),
            'x2': np.tile(np.linspace(self.x2_min, self.x2_max, npts_per_lc), self.nbands),
            'sn': np.zeros(npts).astype(int),
            'band': np.repeat(np.arange(self.nbands), npts_per_lc).astype(int),
            'y': np.zeros(npts),
            'yerr': np.zeros(npts),
            'var': np.zeros(npts),
            'bads': np.zeros(npts).astype(bool)
        }
        d = pandas.DataFrame(d)
        d['wl'] = 1500. * d['band'] + 4000.

        dp = DataProxy(d, x1='x1', x2='x2', sn='sn', band='band', wl='wl', y='y', yerr='yerr', var='var')
        dp.make_index('sn')
        dp.make_index('band')

        return dp

    def generate(self):
        """
        """
        sample = self.gen_sample()
        dp = self.gen_data(sample)
        dp.sample = sample
        return dp
