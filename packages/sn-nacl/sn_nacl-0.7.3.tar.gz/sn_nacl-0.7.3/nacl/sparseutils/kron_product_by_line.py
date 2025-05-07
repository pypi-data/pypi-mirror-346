"""A line-wise Kronecker product of two matrices"""

import logging

import numba
import numpy as np
import scipy


logger = logging.getLogger(__name__)


@numba.njit
def _tile(a, reps):
    """Numba compatible version of np.tile for 1d arrays"""
    # np.tile is not (yet) supported by numba (at version 0.60.0), we use an
    # implementation from https://github.com/numba/numba/pull/5785. Here `a`
    # is assumed to be a 1d array and `resp` a positive integer.
    #
    # NOTE The trivial implementation
    #    np.repeat(a, reps).reshape(-1, a).T.flatten()
    # as proposed in https://stackoverflow.com/a/61703512 has been benchmarked
    # much slower than the following version.
    sz = a.size
    out = np.empty(reps * sz, dtype=a.dtype)
    for i in range(reps):
        start = i * sz
        end = start + sz
        out[start:end] = a
    return out


@numba.njit(parallel=True)
def _kron_product_by_line(a_data, a_indptr, a_indices, b, eliminate_zeros=False):
    """Auxiliary function to `kron_product_by_line`"""
    # for each row i, the starting index where to write in output buffers
    c_indptr = a_indptr * b.shape[1]

    # number of non-zero triplets in result
    c_size = (c_indptr[1:] - c_indptr[:-1]).sum()

    # allocate output buffers
    c_rows = np.empty(c_size, dtype=np.int32)
    c_cols = np.empty(c_size, dtype=np.int32)
    c_vals = np.empty(c_size, dtype=a_data.dtype)

    # for each row (done in parallel by numba)
    for i in numba.prange(a_indptr.shape[0] - 1):
        # start and stop indices of current row's data and column indices
        a_slice = slice(a_indptr[i], a_indptr[i+1])
        c_slice = slice(c_indptr[i], c_indptr[i+1])

        c_rows[c_slice] = i
        c_cols[c_slice] = (
            np.repeat(a_indices[a_slice] * b.shape[1], b.shape[1]) +
            _tile(np.arange(b.shape[1]), a_indptr[i+1] - a_indptr[i]))
        c_vals[c_slice] = np.outer(a_data[a_slice], b[i, :]).flatten()

    # remove any zeros
    if eliminate_zeros:
        mask = c_vals != 0
        return c_rows[mask], c_cols[mask], c_vals[mask]
    return c_rows, c_cols, c_vals


def kron_product_by_line(a, b, eliminate_zeros=False):
    r"""A line-wise Kronecker product of two matrices

    This operation is also called the transposed Khatri-Rao product.

    This function is optimized to compute the product of a sparse matrix `a` in
    CSR format by a dense matrix `b`. If `a` and `b` have different data types,
    the dtype of the output matrix is fixed to the one of `a`.

    Use `eliminate_zeros=True` to remove zero values from the sparse structure
    of the output matrix. They are introduced when `b` contains zeros (the
    number of introduced zeros is `a.shape[1] * (b == 0).sum()`). This is
    usually not required and is very expansive with respect to the main
    computation. This option has been introducted to strictly conform with
    implementation of this function in `sn-nacl<=0.6.0`.

    Parameters
    ----------
    a : (k, n) sparse matrix
        first matrix of the product, must be sparse preferably in CSR format.
        The matrix is converted to CSR format if needed.
    b : (k, m) dense matrix
        second matrix of the product
    eliminate_zeros : bool, optional
        When True, remove zero entries from the returned matrix.

    Returns
    -------
    c : (k, m*n) sparse matrix in COO format
        Line-wise Kronecker product of `a` and `b`

    Raises
    ------
    ValueError
        If `a` and `b` are incompatible or in some invalid format.

    Examples
    --------
    >>> import numpy as np
    >>> import scipy as sp
    >>> from nacl.sparseutils import kron_product_by_line
    >>> a = sp.sparse.csr_matrix(np.array([[0., 2.], [5., 0.]]))
    >>> b = np.array([[1., 2.], [3., 4.]])
    >>> kron_product_by_line(a, b).toarray()
    array([[ 0.,  0.,  2.,  4.],
           [15., 20.,  0.,  0.]])

    """
    if not (a.ndim == 2 and b.ndim == 2):
        raise ValueError("The both arrays should be 2-dimensional.")

    if not a.shape[0] == b.shape[0]:
        raise ValueError(
            "The number of rows for both arrays should be equal.")

    if not scipy.sparse.issparse(a):
        raise ValueError("`a` must be a sparse array.")

    if scipy.sparse.issparse(b):
        raise ValueError("`b` must be a dense array.")

    if a.dtype != b.dtype:
        logger.warning(
            "matrices `a` and `b` have different dtypes (%s and %s), "
            "result computed with dtype %s", a.dtype, b.dtype, a.dtype)

    if a.format != 'csr':
        logger.debug(
            'converting sparse matrix of shape %s from %s to csr format',
            a.shape, a.format)
        a = a.tocsr()

    rows, cols, vals = _kron_product_by_line(
        a.data, a.indptr, a.indices, b, eliminate_zeros=eliminate_zeros)

    return scipy.sparse.coo_matrix(
        (vals, (rows, cols)),
        shape=(a.shape[0], a.shape[1] * b.shape[1]))
