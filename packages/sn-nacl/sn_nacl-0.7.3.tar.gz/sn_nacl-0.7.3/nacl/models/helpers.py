
import scipy.sparse as sparse
import numpy as np
from saltworks.fitparameters import FitParameters


def check_grad(model, pars, dx=1.E-6):
    """
    """
    v, jacobian = model(pars, jac=True)
    pp = pars.copy()
    df = []
    for i in range(len(pp.full)):
        k = pp.indexof(i)
        if k < 0:
            continue
        pp.full[i] += dx
        vp = model(pp, jac=False)
        df.append((vp-v)/dx)
        pp.full[i] -= dx
    return np.array(jacobian.todense()), np.vstack(df).T


def check_deriv(pen, pars, dx=1.E-6):
    """
    """
    v, grad, hess = pen(pars.free, deriv=True)
    pp = pars.copy()

    df, d2f = [], []
    for i in range(len(pp.full)):
        k = pars.indexof(i)
        if k < 0:
            continue
        pp.full[i] += dx
        vp = pen(pp.free, deriv=False)
        pp.full[i] -= (2*dx)
        vm = pen(pp.free, deriv=False)
        df.append((vp-vm)/(2*dx))
        pp.full[i] += dx
    return np.array(grad), np.vstack(df).T


def check_deriv_old(pen, pars, dx=1.E-6):
    """Temporary version, to accomodate the LogLikelihood transitional interface
    """
    v, grad, hess = pen(pars.free, deriv=True)
    pp = pars.copy()

    df, d2f = [], []
    for i in range(len(pp.full)):
        pp.full[i] += dx
        vp = pen(pp.free, deriv=False)
        pp.full[i] -= (2*dx)
        vm = pen(pp.free, deriv=False)
        df.append((vp-vm)/(2*dx))
        pp.full[i] += dx
    return np.array(grad), np.vstack(df).T


def plot_analytical_vs_numerical_derivatives(J, Jn, block_name='', relative=False):
    """
    """
    import pylab as pl
    if block_name is None:
        block_name = ''

    fig, axes = pl.subplots(figsize=(16,4), nrows=1, ncols=2)
    fig.suptitle(block_name)
    axes[0].plot(J.ravel(), Jn.ravel(), 'k.')
    axes[0].set_title(block_name)
    axes[0].set_xlabel('model')
    axes[0].set_ylabel('numerical')

    if relative:
        axes[1].plot(J.ravel(), np.abs((J.ravel()-Jn.ravel())/J.ravel()), 'b.')
        axes[1].set_ylabel('(model - num) / model [relative]')
    else:
        axes[1].plot(J.ravel(), J.ravel()-Jn.ravel(), 'b.')
        axes[1].set_ylabel('model - num')
    axes[1].set_title(block_name)


    fig, axes = pl.subplots(figsize=(16,4), nrows=1, ncols=3)
    fig.suptitle(block_name)
    axes[0].imshow(J, aspect='auto')
    axes[0].set_title('model derivatives')
    axes[1].imshow(Jn, aspect='auto')
    axes[1].set_title('numerical derivatives')
    axes[2].imshow(J-Jn, aspect='auto')
    axes[2].set_title('diff')
