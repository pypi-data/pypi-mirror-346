import numpy as np


class Cache:
    """A cache where the keys are numpy arrays

    Used to cache the results of the model computations, which may be
    computationnaly expensive. The cached values are indexed by the parameter
    vectors.

    This is not a generic class. Used in the models and the Likelohood, where
    you have states which you want to preserve, that are encoded by a vector of
    parameters.

    Why not use a hash ? Because I found that numpy.array_equal is in fact
    faster than hash(str(p)). If someone points me to a faster solution, I'll
    adopt it.

    """
    def __init__(self, max_size=2):
        self.max_size = max_size
        self._cache = []

    def __len__(self):
        return len(self._cache)

    def insert(self, p, blob):
        """insert a blob in cache, with p as a key

        Parameters:
        -----------
        p: (ndarray)
          parameter vector used as a key.
        blob: stuff
          the object to cache

        .. note:: this method does not verify that the key is not already in the
                  cache. If this is the case, then, the older blob will be
                  masked and the older (key,blob) entry will eventually be
                  pushed out of the cache. Note that if there is a value indexed
                  by the same key, then you might have a bug somewhere, because
                  it means that your function returns different values for the
                  same input parameter vector.
        """
        if len(self._cache) == self.max_size:
            self._cache.pop()
        self._cache.insert(0, (p, blob))

    def get(self, p):
        """retrieve a blob indexed by the parameter vector p from the cache

        if no match, return None.

        Parameters
        ----------
        p: (ndarray)
          parameter vector used as a key

        """
        for c in self._cache:
            key, blob = c
            if np.array_equal(p, key):
                return blob
        return None

    def keys(self):
        """return the list of keys in the cache
        """
        ret = [c[0] for c in self._cache]
        return ret
