#!/usr/bin/env python3


import numpy as np
import numpy.polynomial.polynomial as nppol
from scipy import sparse


class CalibPrior:

    def __init__(self, calib_covmat, block_name='eta'):
        self.calib_covmat = calib_covmat
        self.matrix = None
        self.block_name = block_name

    def init_pars(self, pars):
        self.matrix = self.init_w_matrix(pars)

    def init_w_matrix(self, pars):
        """
        """
        W = np.linalg.inv(self.calib_covmat)
        W = sparse.coo_matrix(W)
        pars_full = pars.copy()
        pars_full.release()

        N = len(pars_full.full)
        i = pars[self.block_name].indexof(W.row)
        j = pars[self.block_name].indexof(W.col)
        M = sparse.coo_matrix((W.data, (i,j)), shape=(N,N)).tocsr()

        return M
    
    def __call__(self, pars, deriv=False):
        """
        """
        if self.matrix is None:
            self.matrix = self.init_w_matrix(pars)
        pp = pars.full
        penalty = float(pp.T @ self.matrix @ pp)

        if not deriv:
            return penalty

        n = self.matrix.shape[0]
        idx = pars.indexof(np.arange(n)) >= 0

        grad = 2. * (self.matrix @ pp)[idx]
        hess = 2. * self.matrix[:,idx][idx,:]

        return penalty, grad, hess


class ColorScatterPrior:

    def __init__(self, model, pivot_wl=5000., deg=2):
        """
        """
        self.model = model
        self.pivot_wl = pivot_wl
        self.deg = deg
        self.mean_sn_band_wl = None
        # a piece of code to compute the
        # equivalent wavelength associated to each kappa
        dp = model.data
        self.kappa_wl = np.unique(np.vstack((dp.sn_band_index, dp.wl)).T, axis=0)[:,1]

    def get_struct(self):
        return [('sigma_kappa', self.deg+1)]

    def init_pars(self, pars):
        """init the sigma-kappa parameters
        """
        pars['sigma_kappa'].full[:] = 1.E-6
        pars['sigma_kappa'].full[0] = -4.

    def __call__(self, pars, deriv=False):
        """evaluate the color scatter penalty (along with its derivatives)
        """
        sigma_kappa = pars['sigma_kappa'].full
        kappa = pars['kappa'].full

        # variance model
        rwl = (self.kappa_wl - self.pivot_wl) / self.pivot_wl
        var = np.exp(nppol.Polynomial(sigma_kappa)(rwl))

        # log det, penaly
        log_det = np.log(var).sum()
        quad_penalty = (kappa**2 / var).sum()
        penalty = log_det + quad_penalty

        if not deriv:
            return penalty

        # gradient w.r.t kappa
        N = len(pars.free)
        grad = np.zeros(N)
        j = pars['kappa'].indexof()
        idx = j>=0
        grad[j[idx]] = (2. * kappa / var)[idx]

        # gradient w.r.t sigma_kappa
        nk = len(pars['kappa'].full)
        ns = len(pars['sigma_kappa'].full)
        var = var.reshape(-1,1)
        kappa = kappa.reshape(-1,1)
        dq_ds = nppol.polyvander(rwl, deg=self.deg)
        tr_wdv =  np.sum(dq_ds, axis=0)
        kwdvwk = -np.sum(kappa**2 * dq_ds / var, axis=0)
        print(tr_wdv, kwdvwk)
        j = pars['sigma_kappa'].indexof()
        idx = j >= 0
        # check the signs
        grad[j[idx]] = (-tr_wdv - kwdvwk)[idx]

        # hessian w.r.t kappa
        i, j, val = [], [], []
        m = sparse.coo_matrix(np.diag(2. / var.flatten()), shape=(nk,nk))
        i.append(pars['kappa'].indexof(m.row))
        j.append(pars['kappa'].indexof(m.col))
        val.append(m.data)

        # hessian: kappa-sigma_kappa block
        m = sparse.coo_matrix(-2. * kappa * dq_ds / var, shape=(nk,ns)) # was -2
        i.append(pars['kappa'].indexof(m.row))
        j.append(pars['sigma_kappa'].indexof(m.col))
        val.append(m.data)
        j.append(pars['kappa'].indexof(m.row))
        i.append(pars['sigma_kappa'].indexof(m.col))
        val.append(m.data)

        # hessian: sigma_kappa - sigma_kappa block
        dq = kappa * dq_ds / np.sqrt(var)
        # tr_wdvwdv = -4 * dq.T @ dq
        # dq = kappa**2 * dq_ds / sig
        kwdvwdvwk = dq.T @ dq
        m = sparse.coo_matrix(kwdvwdvwk, shape=(ns,ns))
        i.append(pars['sigma_kappa'].indexof(m.row))
        j.append(pars['sigma_kappa'].indexof(m.col))
        val.append(m.data)

        # kk = dsig_ds / sig
        # tr_wdvwdv = -4 * kk.T @ kk
        # kk = kappa * dsig_ds / sig**2
        # kwdvwdvwk = 6 * kk.T @ kk

        # m = sparse.coo_matrix(tr_wdvwdv + kwdvwdvwk)
        # i.append(pars['sigma_kappa'].indexof(m.row))
        # j.append(pars['sigma_kappa'].indexof(m.col))
        # val.append(m.data)

        # encapsulate all that into the (much larger) parameter vector space
        i = np.hstack(i)
        j = np.hstack(j)
        val = np.hstack(val)
        idx = (i>=0) & (j>=0)
        n_free_pars = len(pars.free)
        hessian = sparse.coo_matrix((val[idx], (i[idx], j[idx])), shape=(n_free_pars, n_free_pars))

        return penalty, grad, hessian
