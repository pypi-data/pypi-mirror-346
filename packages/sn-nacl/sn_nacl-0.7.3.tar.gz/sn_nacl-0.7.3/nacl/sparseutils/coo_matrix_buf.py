import logging

import numpy as np
import scipy


logger = logging.getLogger(__name__)


class CooMatrixBuff:
    def __init__(self, shape, estimated_nnz, increment=1.3):
        self.shape = shape
        self.size = estimated_nnz
        self.increment = increment
        self.i = np.zeros(self.size).astype(np.int64)
        self.j = np.zeros(self.size).astype(np.int64)
        self.val = np.zeros(self.size)
        self.ptr = 0

    def _resize(self):
        logger.warning(
            'need to resize CooMatrixBuff: revise your estimates of non-zero terms !')
        new_size = self.size * self.increment
        self.i = np.resize(self.i, new_size)
        self.j = np.resize(self.j, new_size)
        self.val = np.resize(self.val, new_size)
        self.i[self.ptr:] = 0
        self.j[self.ptr:] = 0
        self.val[self.ptr:] = 0.
        self.size = new_size

    def append(self, i, j, val, free_pars_only=False):
        """
        """
        logger.info(f'appending {len(i)} to buffer at location {self.ptr}')
        sz = len(i)
        assert (len(j) == sz) and (len(val) == sz)

        if (self.ptr + sz) > self.size:
            self._resize()

        # if free_pars_only:
        #     sz = lib.append(
        #         len(i), self.ptr,
        #         i.astype(np.int64), j.astype(np.int64), val,
        #         self.i, self.j, self.val,
        #         1)
        #     self.ptr += sz
        # else:
        #     sz = lib.append(
        #         len(i), self.ptr,
        #         i.astype(np.int64), j.astype(np.int64), val,
        #         self.i, self.j, self.val,
        #         0)
        #     self.ptr += sz

        if free_pars_only:
            idx = j >= 0
            sz = idx.sum()
            self.i[self.ptr:self.ptr+sz] = i[idx]
            self.j[self.ptr:self.ptr+sz] = j[idx]
            self.val[self.ptr:self.ptr+sz] = val[idx]
            self.ptr += sz
        else:
            self.i[self.ptr:self.ptr+sz] = i
            self.j[self.ptr:self.ptr+sz] = j
            self.val[self.ptr:self.ptr+sz] = val
            self.ptr += sz
        logger.info('done')

    def tocoo(self):
        return scipy.sparse.coo_matrix(
            (self.val[:self.ptr], (self.i[:self.ptr], self.j[:self.ptr])),
            self.shape)


class CooMatrixBuff2:
    def __init__(self, shape, increment=1.3):
        self.shape = shape
        self.increment = increment
        self._row = []
        self._col = []
        self._data = []
        self._idx = []

    def append(self, i, j, val):
        """
        """
        self._row.append(i)
        self._col.append(j)
        self._data.append(val)
        self._idx.append(j>=0)

    def tocoo(self):
        idx = np.hstack(self._idx)
        r = scipy.sparse.coo_matrix(
            (np.hstack(self._data)[idx],
             (np.hstack(self._row)[idx], np.hstack(self._col)[idx])),
            self.shape)
        return r

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @property
    def data(self):
        return self._data
