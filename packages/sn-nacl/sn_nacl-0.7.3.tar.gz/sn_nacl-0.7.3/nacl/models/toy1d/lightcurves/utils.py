"""
"""

import numpy as np
# from scipy import sparse
# from sksparse import cholmod

import pandas
from saltworks import DataProxy
from bbf.bspline import BSpline



def gaussian(x, sigma):
    """
    Gaussian function *2
    """
    # norm = a / (np.sqrt(2. * np.pi) * sigma)
    xx = x / sigma
    return np.exp(-0.5 * xx**2)


class ToyModelGenerator:

    def __init__(self, nsn=100, npts=10, nbands=1,
                 xmin=-10., xmax=10., delta=10.,
                 yerr=0.01,
                 error_pedestal=None, error_snake=None,
                 wl_pivot=5000.,
                 v_calib=0.005**2, color_scatter=np.array([0.02, 0., 0.002])):
        """
        .. note::
           error snake and error_pedestal are mutually exclusive.
           if error_snake > 0, then error_pedestal is set to zero
        """
        self.nsn = nsn
        self.npts = npts
        self.nbands = nbands
        self.xmin = xmin
        self.xmax = xmax
        self.delta = delta
        self.yerr = yerr
        self.error_pedestal = 0.
        self.error_snake = 0.
        if error_pedestal is not None:
            self.error_pedestal = error_pedestal
        if error_snake is not None and error_snake > 0.:
            self.error_pedestal = 0.
            self.error_snake = error_snake
        self.wl_pivot = wl_pivot
        self.band_wl = 1500 * np.arange(nbands) + 4000.
        self.v_calib = v_calib
        if type(v_calib) is float:
            self.v_calib = np.diag(np.full(self.nbands, v_calib))
        self.color_scatter = color_scatter

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
            tmax = np.random.uniform(self.xmin+5, self.xmax-5, size=self.nsn)
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
        npts = self.nsn * self.nbands * self.npts
        d = {
            'x': np.random.uniform(self.xmin, self.xmax, npts),
            'sn': np.repeat(np.arange(self.nsn), self.nbands * self.npts),
            'band': np.tile(np.repeat(np.arange(self.nbands), self.npts), self.nsn),
            'y': np.zeros(npts),
            'yerr': np.zeros(npts),
        }

        for band in self.lcpars:
            d['wl'] = 1500. * d['band'] + 4000.
            dwl = (d['wl'] - self.wl_pivot) / self.wl_pivot
            cl = 1. + dwl * sample.color[d['sn']]
            dt, sigma = self.lcpars[band]
            ph = (d['x']-sample.tmax[d['sn']]-dt) * (1. + sample.stretch[d['sn']])
            d['y'] = sample.x0[d['sn']] * gaussian(ph, sigma) * cl
            d['y_true'] = d['y']
            d['yerr'] = sample.x0[d['sn']] * np.full(npts, self.yerr)
            d['var'] = np.sqrt(self.error_pedestal**2 + self.error_snake**2 * d['y']**2)

        d = pandas.DataFrame(d)
        d['sn_band'] = d.sn * 100 + d.band

        # we need to index the sn_band couples to generate the color scatter
        dp = DataProxy(d, x='x', sn='sn', band='band', sn_band='sn_band',
                       wl='wl', y='y', yerr='yerr', var='var', y_true='y_true')
        dp.make_index('sn_band')

        # add correlated noise
        if self.v_calib is not None:
            L = np.linalg.cholesky(self.v_calib)
            eta = np.random.normal(0., scale=1., size=self.nbands)
            calib_scatter = L @ eta
            d['calib_scatter'] = 1. + calib_scatter[d.band]
            d['y'] *= d.calib_scatter

        if self.color_scatter is not None:
            wl = np.unique(np.vstack((dp.sn_band_index, dp.wl)).T, axis=0)[:,1]
            rwl = (wl - self.wl_pivot) / self.wl_pivot
            sig = np.polynomial.polynomial.Polynomial(self.color_scatter)(rwl)
            kappa = np.random.normal(0., scale=sig)
            d['color_scatter'] = 1. + kappa[dp.sn_band_index]
            d['y'] *= d.color_scatter

        # finally, add some uncorrelated noise
        sig = np.sqrt(d.yerr**2 + self.error_pedestal**2 + self.error_snake**2 * d['y']**2)
        d['noise'] = np.random.normal(scale=sig, size=len(sig))
        d.y += d['noise']

        # final dataproxy, with the final indexes
        dp = DataProxy(d, x='x', sn='sn', band='band', sn_band='sn_band',
                       wl='wl', y='y', yerr='yerr', var='var', y_true='y_true')
        dp.add_field('bads', np.zeros(len(dp.nt)).astype(bool))
        dp.make_index('sn')
        dp.make_index('band')
        dp.make_index('sn_band')

        return dp

    def gen_fine_grid(self, npts_per_lc=100):
        """
        """
        npts = 1 * self.nbands * npts_per_lc
        d = {
            'x': np.tile(np.linspace(self.xmin, self.xmax, npts_per_lc), self.nbands),
            'sn': np.zeros(npts).astype(int),
            'band': np.repeat(np.arange(self.nbands), npts_per_lc).astype(int),
            'y': np.zeros(npts),
            'yerr': np.zeros(npts),
            'var': np.zeros(npts),
            'bads': np.zeros(npts).astype(bool)
        }
        d = pandas.DataFrame(d)
        d['wl'] = 1500. * d['band'] + 4000.
        d['sn_band'] = d.sn * 100 + d.band

        dp = DataProxy(d, x='x', sn='sn', band='band', sn_band='sn_band', wl='wl', y='y', yerr='yerr', var='var')
        dp.make_index('sn')
        dp.make_index('band')
        dp.make_index('sn_band')

        return dp
    
    def generate(self):
        """
        """
        sample = self.gen_sample()
        dp = self.gen_data(sample)
        dp.sample = sample
        dp.band_wl = self.band_wl
        return dp
    def change_noise(self, dp):
        if self.v_calib is not None:
            L = np.linalg.cholesky(self.v_calib)
            eta = np.random.normal(0., scale=1., size=self.nbands)
            calib_scatter = L @ eta
            dp.nt.calib_scatter = 1. + calib_scatter[dp.band]
            dp.y = dp.y_true * dp.nt.calib_scatter
        sig = np.sqrt(dp.yerr**2 + dp.var**2)/5
        noise = np.random.normal(scale=sig, size=len(sig))
        dp.y = dp.y_true + noise
