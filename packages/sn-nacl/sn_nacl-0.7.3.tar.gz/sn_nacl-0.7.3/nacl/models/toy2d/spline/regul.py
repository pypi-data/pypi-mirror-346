

import numpy as np
from scipy import sparse



class Regularization:
    """Regularization penalty

    TODO: it would be a good idea if the adaptive regularization was performed
    here. Or at least if there was a method to do it on the fly here.

    .. note:: in order to save time, the regularization matrix is precomputed.
              This means that whenever the structure of the parameter vector is
              modified (i.e. blocks are added or removed), it should be
              recomputed. Note that it does not apply to the fact that we fix or
              free parameters.

    """
    def __init__(self, nj, block_name='theta', mu0=2., mu2=1.):
        """
        """
        self.block_name = block_name
        self.mu0 = mu0
        self.mu2 = mu2
        self.matrix = None
        self.reg_lambda = None # adaptive regularization
        self.nj = nj
    def init_pars(self, pars):
        """
        """
        self.matrix = self.init_reg_matrix(pars)

    def init_reg_matrix(self, pars):
        """precompute the full regularization  matrix
        This gives that by default :math:`P_{\theta_{0|1}}` is given by:
        
        2nd degree matrix looks like this (P = p.T @ p) where is the 2nd derivative
        of theta_i_j (laplacian)


        """
        # reset reg_matrix and adaptive regularization
        self.matrix = None#
        self.reg_lambda = None

        pars_full = pars.copy()
        pars_full.release()

        n = len(pars_full[self.block_name].full)
        N = len(pars_full.full)

        # order 0
        P = sparse.dia_matrix((np.ones(N), [0]), shape=(n, n)).tocoo()
        i = pars_full.indexof(P.row)
        j = pars_full.indexof(P.col)
        P = sparse.coo_matrix((P.data, (i,j)), shape=(N,N))

        # second order penality, from the laplacian matrix and slightly hacked
        # to make the end of the diagonal similar to the beginning
        
        
        #data = np.ones((n,3))
        #data[:,1] = -2
        #Q = sparse.dia_matrix((data.T, [0,1,2]), shape=[n,n]).tocoo()
        # print(Q.todense())
        #i = pars_full.indexof(Q.row)
        #j = pars_full.indexof(Q.col)
        #Q = sparse.coo_matrix((Q.data, (i,j)), shape=(N,N))
        #A = (Q.T @ Q).tolil()
        #B = A[:3,:3]
        #A[-3:,-3:] = B[::-1,::-1]
        
        nj = self.nj
        data = np.ones((n,6))
        data[:,0] = 4
        data[:,1] = -4
        data[:,3] = -4
        data[:,4] = 2
        Q = sparse.dia_matrix((data.T, [0,1,2, nj, nj+1, 2*nj]), shape=[n,n]).tocoo()
        # print(Q.todense())
        i = pars_full.indexof(Q.row)
        j = pars_full.indexof(Q.col)
        Q = sparse.coo_matrix((Q.data, (i,j)), shape=(N,N))
        A = (Q.T @ Q).tolil()
        #B = A[:3,:3]
        #A[-3:,-3:] = B[::-1,::-1]
        B = A[:n-nj,:n-nj]
        A[-n+nj:,-n+nj:] = B[::-1,::-1]

        return self.mu0 * P + self.mu2 * A
    
    def adapt_regularization_strength(self, J_model, mu=1., mu_model=1.E-6):
        """
        """
        J = J_model
        cols = np.arange(J.shape[1])
        bins = np.arange(-0.5, J.shape[1]+0.5, 1.)
        d = np.digitize(J.col, bins, right=False) - 1
        l = np.array([0. if (d==col).sum() == 0 else J.data[d==col].max() for col in cols])
        idx = l<0.5
        l[idx] = mu
        l[~idx] = mu_model
        self.reg_lambda = l

        L = sparse.dia_matrix((l, [0]), shape=self.matrix.shape)
        self.matrix = self.matrix @ L

        #        import matplotlib.pyplot as plt
        #        plt.figure()
        #        plt.plot(l, 'k.')

    
    def __call__(self, pars, deriv=False):
        """
        """
        if self.matrix is None:
            self.matrix = self.init_reg_matrix(pars)

        pp = pars.full
        penalty = pp.T @ self.matrix @ pp

        if not deriv:
            return penalty

        n = self.matrix.shape[0]
        idx = pars.indexof(np.arange(n)) >= 0

        grad = 2. * (self.matrix @ pp)[idx]
        hess = 2. * self.matrix[:,idx][idx,:]

        return penalty, grad, hess
