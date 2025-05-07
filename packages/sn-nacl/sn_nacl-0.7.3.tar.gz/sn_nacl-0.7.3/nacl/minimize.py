"""
This module is a rewrite of the minimizers.py module.
"""

import logging
import sys
import time

import numpy as np
import scipy
import scipy.optimize
import scipy.sparse.linalg as lg
import pandas
import matplotlib.pyplot as plt

from sksparse import cholmod

#pylint: disable=logging-fstring-interpolation
#pylint: disable=too-many-locals
#pylint: disable=c-extension-no-member

logger = logging.getLogger(__name__)

if 'sparse_dot_mkl' in sys.modules:
    logger.info('sparse_dot_mkl found. Building hessian should be faster.')
else:
    logger.warning('module: `sparse_dot_mkl` not available')

def cond_number(A):
    """ from scipy arpack
    """
    ew1, _ = lg.eigsh(A, which='LM')
    ew2, _ = lg.eigsh(A, sigma=1e-8)
    return np.abs(ew1).max()/np.abs(ew2).min()


class Minimizer:
    """Find the minimum of a function using a Levenberg Marquard method"""
    def __init__(self, log_likelihood, max_iter=100,
                 dchi2_stop=0.001, log=None):
        self.log_likelihood = log_likelihood
        # self.model = self.log_likelihood.model
        self.max_iter = max_iter
        self.dchi2_stop = dchi2_stop
        if log is None:
            log = []
        self._log = log

    def ndof(self):
        """ Return number of degrees of freedom.
        """
        # return self.model.training_dataset.nb_meas() - len(self.model.pars.free)
        return self.log_likelihood.ndof()

    def get_log(self):
        """ Return logged quantities as a panda DataFrame.
        """
        return pandas.DataFrame(self._log)

    def minimize_lm(self, p_init, **kwargs):
        """The Levenberg Marquard version of minimize

        Parameters
        ----------
        dchi2_stop: float, default: 1.E-3
          stop criterion.
        mode: {'supernodal', 'simplicial'}, default: 'supernodal'
          cholmod algorithm.
        ordering_method: str, default: 'metis'
          ordering method.
        beta: float, default: 0.
          whether to surcharge the hessian diagonal before factorizing.
        lamb: float, default: 1.E-3
          the initial value of the LM damping parameter.
        accept: float, default: 10.
          factor applied on lambda if the step is accepted
        reject: float, default: 5.
          factor applied on lambda if the step is rejected
        max_iter: int, default:100
          maximum number of iterations before we give up

        Returns
        -------
        dict containing 'pars', 'chi2', 'ndof', and 'status'
        """

        #pylint: disable=too-many-branches
        #pylint: disable=too-many-statements

        # it has to be a copy !
        # pars = self.model.pars.copy()
        pars = self.log_likelihood.pars.copy()
        pars.free = p_init
        dchi2_stop = kwargs.get('dchi2_stop', self.dchi2_stop)
        # dpars = self.model.pars.copy()
        dpars = self.log_likelihood.pars.copy()
        dpars.full[:] = 0.
        self._log = []

        old_pars = pars.copy()
        trial = pars.copy()
        mode = kwargs.get('mode', 'supernodal')
        ordering_method = kwargs.get('ordering_method', 'metis')
        beta = kwargs.get('beta', 0.)

        accept = kwargs.get('accept', 10.)
        reject = kwargs.get('reject', 10.)

        # number of tries to get a correct LM step
        max_attempts = kwargs.get('max_attempts', 100)
        # maximum number of iterations allowed
        max_iter = kwargs.get('max_iter', self.max_iter)
        lamb = kwargs.get('lamb', 1.E-3)

        # diag_charge
        diag_charge = kwargs.get('diag_charge', 'levenberg')

        # minimization loop
        for i in range(max_iter+1):
            # logger.info(f'minimize_lm: {i}')
            chi2, grad, hessian = self.log_likelihood(pars.free, deriv=True)
            # r0 = self.log_likelihood.w_res

            #just a test to see whether the raw hessian is or not posdef
            try:
                fact = cholmod.cholesky(hessian.tocsc(),
                                        mode=mode,
                                        ordering_method=ordering_method,
                                        beta=beta)
            except cholmod.CholmodNotPositiveDefiniteError:
                logger.warning('raw hessian not posdef')

            if i == 0:
                logger.info(
                    f'init: l={lamb:6.1e} chi2: {chi2:12.4e} ndof={self.ndof()} '
                    f'chi2/ndof={chi2/self.ndof()}')

            # LM step
            diag_max = None
            success, attempts = False, 0
            while not success:
                if attempts == max_attempts:
                    logger.error('unable to get a valid LM step')
                    return {'pars': pars.copy(),
                            'chi2': chi2,
                            'ndof': self.ndof(),
                            'status': 'no valid LM step'}

                try:
                    diag = hessian.diagonal()
                    diag_max = diag if diag_max is None else np.maximum(diag_max, diag)
                    diag_max = np.maximum(1.E-6, diag_max)
                    zero_idx = diag <= 0.
                    if zero_idx.sum() > 0:
                        logging.warning(f'zero Hessian diagonal coefficients'
                                        f'{np.where(zero_idx)[0]}')
                    if diag_charge == 'levenberg':
                        hessian.setdiag(diag + lamb)
                    elif diag_charge == 'marquardt':
                        hessian.setdiag((1.+lamb) * diag)
                    elif diag_charge == 'marquardt_max':
                        # max_diag = diag.max()
                        hessian.setdiag(diag + lamb * diag.max())
                    elif diag_charge == 'marquardt_lmax':
                        hessian.setdiag(diag + lamb * diag_max)
                    else:
                        raise ValueError(f'diag_charge: invalid value {diag_charge}')

                    fact = cholmod.cholesky(hessian.tocsc(),
                                            mode=mode,
                                            ordering_method=ordering_method,
                                            beta=beta)

                    # NOTE: rectifying the algebra.
                    # if the log-likelohood returns its true gradient,
                    # the NR-step is H^-1 @ (-grad)
                    dpars.free = fact(-1. * grad)
                    hessian.setdiag(diag)
                except cholmod.CholmodNotPositiveDefiniteError:
                    logger.error('cholesky failed: matrix non posdef')
                    lamb *= reject
                    attempts += 1
                    continue

                # print(dpars)

                # old_chi2 = chi2
                # old_pars.free = pars.free
                # pars.free = pars.free + dpars.free
                trial.free = pars.free + dpars.free
                # if geo:
                #     trial.free += geo_corr

                # check_chi2 = self.log_likelihood(pars.free, deriv=False)
                trial_chi2 = self.log_likelihood(trial.free, deriv=False)
                # print(f'CHECK: {chi2} {check_chi2} {trial_chi2}')
                dchi2 = chi2 - trial_chi2

                # if geo and truncerr > 2.:
                #     pass
                if dchi2 > 0.  or (np.abs(dchi2) <= dchi2_stop):
                    success = True
                else:
                    pass

                # if dchi2 > 0. or (np.abs(dchi2) <= dchi2_stop):
                if success:
                    lamb /= accept
                    # logger.info(f'success: dchi2={dchi2}')
                else:
                    lamb *= reject
                    # chi2 = self.log_likelihood(pars.free, deriv=False)
                    logger.warning(f'[{attempts}/{max_attempts}] '
                                   f'increasing chi2: dchi2={dchi2:.4e} '
                                   f'next attempt with lambda={lamb:.4e}')
                    attempts += 1
                    continue

            # now, we can update the parameter vector
            old_chi2 = chi2
            chi2 = trial_chi2
            old_pars.free = pars.free
            pars.free = trial.free

            # if logger activated, we construct a log structure here
            l = self.log_likelihood.get_log()
            l['step'] = i
            l['time'] = time.perf_counter()
            l['lambda'] = lamb
            l['dchi2'] = dchi2
            l['attempts'] = attempts
            l['ldpars'] = np.sqrt(np.dot(dpars.free, dpars.free))
            l['dpars'] = dpars.copy()
            self._log.append(l)

            return_dict = {'pars': pars.copy(),
                           'chi2': chi2,
                           'ndof': self.ndof()}
            # maybe we have converged ?
            if np.abs(dchi2) <= dchi2_stop:
                logger.info(f'converged: dchi2={dchi2:12.4e}: {old_chi2:12.4e} -> {chi2:12.4e} '
                            f'ndof={self.ndof()} chi2/ndof={chi2/self.ndof():.6f}')
                return_dict["status"] = 'converged'
                return return_dict

            logger.info(f'iter {i: 3d} l={lamb:6.1e}: {old_chi2:12.4e} -> {chi2:12.4e} '
                        f'| dchi2={dchi2:12.4e} | ndof={self.ndof()} '
                        f'chi2/ndof={chi2/self.ndof():.6f}')


        return_dict["status"] = 'too many interations'
        return return_dict




    def get_cov_matrix(self, params_of_interest=None, corr=False, plot=False):
        """
        returns the covariance matrix and correlation matrix and the estimated
        errors on the parameters of interest
        cov : V
        corr : Vij/sqrt(Vii*Vjj)
        and can plot them

        Return:
        V : covariance matrix
        err_of_interest (optional) : errors on the specified parameters
        corr (optional) : correlation matrix
        """
        _, _, H = self.log_likelihood(self.log_likelihood.pars.free, deriv=True)
        try:
            f = cholmod.cholesky(H, mode='supernodal', ordering_method='metis')
        except cholmod.CholmodError:
            try:
                logger.info('ADDING BETA=1e-6')
                f = cholmod.cholesky(H, mode='supernodal', ordering_method='metis', beta=1e-6)
            except cholmod.CholmodError:
                logger.info("using diag charge")
                diag = H.diagonal()
                lamb = self.get_log()['lambda'].iloc[-1]
                H.setdiag(diag + 10 * lamb * diag.max())
                f = cholmod.cholesky(H.tocsc(), mode='supernodal', ordering_method='metis')

        V = 2 * f.inv()
        var = V.diagonal()
        index_of_interest = np.array([])
        if plot:
            plt.figure()
            plt.imshow(V.toarray())
            plt.colorbar()
            plt.title('Covariance matrix')
        if params_of_interest is not None:
            for x in params_of_interest:
                idx = self.log_likelihood.pars.indexof(x)
                index_of_interest = np.append(index_of_interest, idx)
                if plot:
                    plt.figure()
                    plt.imshow(V.toarray()[idx][:,idx])
                    plt.colorbar()
                    plt.title('Covariance matrix of ' + x)
            index_of_interest = index_of_interest.astype(int)
            err_of_interest = np.sqrt(var[index_of_interest])
        else:
            err_of_interest = None
        if not corr:
            return V, err_of_interest
        N = len(var)
        i = np.arange(N)
        ii = np.vstack([i for k in range(N)])
        v1 = var[ii]
        v2 = v1.T
        vii_jj = v1 * v2
        vii_jj = np.sqrt(vii_jj)
        corr = V/vii_jj
        if plot:
            plt.figure()
            plt.imshow(corr.toarray())
            plt.colorbar()
            plt.title('Correlation matrix')
        return V, err_of_interest, corr


    def plot(self, timesteps=False, output_file=None):
        """ Plot logged quantities.

        Parameters
        ----------
        timesteps: bool, default: False
          x axis is elapsed time rather than iteration number.
        output_file: str, default: None
          if not None, save figure in this file.
        """
        if not hasattr(self, '_log'):
            return
        d = pandas.DataFrame(self._log)
        fig, axes = plt.subplots(nrows=8, ncols=1, figsize=(6,12), sharex=True)
        xx = d.step if not timesteps else d.time-d.time.min()
        xlabel = 'step' if not timesteps else 'time [s]'
        axes[0].plot(xx, d.llk, 'k.:')
        axes[0].set_ylabel(r'$-2\ln {\cal L}$')
        axes[1].semilogy(xx, d.main_chi2, 'b.:')
        axes[1].set_ylabel(r'$\chi^2$')
        axes[2].plot(xx, d.log_det_v, 'r.:')
        axes[2].set_ylabel(r'$\log\|\mathbf{V}\|$')
        axes[3].semilogy(xx, d.reg, 'g.:')
        axes[3].set_ylabel('reg')
        axes[4].semilogy(xx, d.cons, 'g.:')
        axes[4].set_ylabel('cons')
        axes[5].semilogy(xx, d.dchi2, 'b.:')
        axes[5].set_ylabel(r'$\delta -2\ln {\cal L}$')
        axes[5].set_xlabel(xlabel)
        plt.subplots_adjust(wspace=0.005, hspace=0.005)
        axes[6].semilogy(xx, d["lambda"], 'k.:')
        axes[6].set_ylabel(r'$\lambda$')
        axes[7].plot(xx, d.attempts, 'k.:')
        axes[7].set_ylabel(r'attempts')
        if output_file is not None:
            fig.savefig(output_file, bbox_inches='tight')



class WeightedResiduals:
    """Return residuals weighted by measurement errors and variance
    model.
    """
    #pylint: disable=too-few-public-methods
    def __init__(self, model, variance_model=None):
        """iniate the residual function"""
        self.model = model
        self.training_dataset = model.training_dataset
        self.variance_model = variance_model
        self.y = self.training_dataset.get_all_fluxes()
        self.yerr = self.training_dataset.get_all_fluxerr()

    def __call__(self, p, jac=False):
        """evaluate"""
        self.model.pars.free = p

        # evaluate the residuals
        val, J = None, None
        if jac:
            val, J = self.model(p, jac=True)
        else:
            val = self.model(p, jac=False)
        res = self.y - val

        # measurement variance and weights
        var, Jvar = 0., None
        if self.variance_model is not None:
            if not jac:
                var = self.variance_model(p, jac=False)
            else:
                var, Jvar = self.variance_model(p, jac=True)

        res_var = self.yerr**2 + var
        w = 1. / np.sqrt(res_var)
        N = len(self.y)
        W = scipy.sparse.dia_matrix((w, [0]), shape=(N, N))

        # weighted residuals
        wres = W @ res
        if jac:
            wJ = W @ J
            return wres, wJ, Jvar
        return wres
