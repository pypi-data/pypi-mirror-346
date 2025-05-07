import numpy as np
import pytest
import scipy

from nacl.sparseutils.kron_product_by_line import kron_product_by_line
from bbf.bspline import BSpline


def test_wont_work():
    with pytest.raises(ValueError) as err:
        kron_product_by_line(
            np.asarray([1., 2.]),
            np.asarray([1., 2.]))
    assert "both arrays should be 2-dimensional" in str(err)

    with pytest.raises(ValueError) as err:
        kron_product_by_line(
            np.asarray([1., 2.]).reshape(1, 2),
            np.asarray([1., 2.]))
    assert "both arrays should be 2-dimensional" in str(err)

    with pytest.raises(ValueError) as err:
        kron_product_by_line(
            np.asarray([1., 2.]).reshape(1, 2),
            np.asarray([1., 2., 3., 4.]).reshape(2, 2))
    assert "number of rows for both arrays should be equal" in str(err)

    A = scipy.sparse.csr_matrix(
        np.asarray([1., 2., 3., 4.]).reshape((2, 2)))
    B = np.asarray([0., 5., 6., 7.]).reshape((2, 2))

    with pytest.raises(ValueError) as err:
        kron_product_by_line(B, B)
    assert "must be a sparse array" in str(err)

    with pytest.raises(ValueError) as err:
        kron_product_by_line(A, A)
    assert "must be a dense array" in str(err)


@pytest.mark.parametrize('dtype', (np.float32, np.float64))
def test_kron_product_by_line_1(dtype):
    A = scipy.sparse.csr_matrix(
        np.asarray([1, 2, 3, 4]).reshape((2, 2)).astype(dtype))
    B = np.asarray([0, 5, 6, 7]).reshape((2, 2)).astype(np.float64)

    # C has the same dtype as A
    C = kron_product_by_line(A, B)
    assert C.shape == (2, 4)
    assert C.dtype == dtype
    assert np.allclose(
        C.toarray().flatten(),
        np.asarray([0, 5, 0, 10, 18, 21, 24, 28], dtype=dtype))


def test_kron_product_by_line_2():
    A = scipy.sparse.csr_matrix(
        np.asarray([1, 2, 3, 4]).reshape((2, 2)).astype(np.float64))
    B = np.asarray([0, 5, 6, 7]).reshape((2, 2)).astype(np.float64)

    C1 = kron_product_by_line(A, B, eliminate_zeros=False)
    C2 = kron_product_by_line(A, B, eliminate_zeros=True)

    assert C1.shape == C2.shape == (2, 4)
    assert C1.dtype == C2.dtype == np.float64
    assert np.allclose(
        C1.toarray().flatten(),
        np.asarray([0, 5, 0, 10, 18, 21, 24, 28], dtype=np.float64))
    assert np.allclose(C1.toarray(), C2.toarray())

    # we have 2 zeros introduced in C1
    assert len(C1.data) == len(C2.data) + 2
    C1.eliminate_zeros()
    assert len(C1.data) == len(C2.data)
    assert np.allclose(C1.toarray(), C2.toarray())


def test_kron_product_by_line_3():
    basis = BSpline(np.linspace(-10., 10., 3))
    J = basis.eval(np.asarray([0.1, 0.3, 0.2]))
    assert J.shape == (3, 5)

    F = np.asarray(
        [0.2, 0.1, 0.3, 0, 0, 0.5, 1, 1.2, 0, 0.1, 0, 0, 0, 0, 0]
    ).reshape((3, 5))

    K = kron_product_by_line(J, F)
    assert K.shape == (3, 25)

    expected = scipy.sparse.coo_matrix((
        [3.23433000e-02, 1.61716500e-02, 4.85149500e-02, 1.33313433e-01,
         6.66567167e-02, 1.99970150e-01, 3.43432333e-02, 1.71716167e-02,
         5.15148500e-02, 3.33333333e-08, 1.66666667e-08, 5.00000000e-08,
         7.60560833e-02, 1.52112167e-01, 1.82534600e-01, 1.52112167e-02,
         3.32890083e-01, 6.65780167e-01, 7.98936200e-01, 6.65780167e-02,
         9.10515833e-02, 1.82103167e-01, 2.18523800e-01, 1.82103167e-02,
         2.25000000e-06, 4.50000000e-06, 5.40000000e-06, 4.50000000e-07],
        ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [5, 6, 7, 10, 11, 12, 15, 16, 17, 20, 21, 22, 5, 6, 7, 9, 10,
          11, 12, 14, 15, 16, 17, 19, 20, 21, 22, 24])), shape=(3, 25)).toarray()
    assert np.allclose(K.toarray(), expected)
