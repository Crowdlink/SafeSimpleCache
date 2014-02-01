# -*- coding: utf-8 -*-
"""
    Implements a simple thread safe cache for Flask

    :copyright: (c) 2014 Isaac Cook
    :license: BSD, see LICENSE for more details
"""

__version__ = '0.1'
__versionfull__ = __version__

from time import time
try:
    import cPickle as pickle
except ImportError:  # pragma: no cover
    import pickle

from werkzeug.contrib.cache import BaseCache
from flask_ssc.synch import RWLock


class SafeSimpleCache(BaseCache):
    """Simple memory cache for multi process environments.

    :param threshold: the maximum number of items the cache stores before
                      it starts deleting some.
    :param default_timeout: the default timeout that is used if no timeout is
                            specified on :meth:`~BaseCache.set`.
    :param pickle: Allows disabling of automatic pickle action if you're just
                     storing basic python objects.
    """

    def __init__(self, threshold=500, default_timeout=300, pickle=True):
        BaseCache.__init__(self, default_timeout)
        self._cache = {}
        self._threshold = threshold
        self._pickle = pickle
        self._lock = RWLock()

    def _setial(self, val):
        if self._pickle:
            return pickle.dumps(val, pickle.HIGHEST_PROTOCOL)
        return val

    def _deserial(self, val):
        if self._pickle:
            return pickle.loads(val)
        return val

    def clear(self):
        with self._lock.writer():
            self._cache.clear()
        return True

    def _prune(self):
        with self._lock.reader():
            length = len(self._cache)
        if length > self._threshold:
            now = time()
            with self._lock.writer():
                for idx, (key, (expires, _)) in enumerate(self._cache.items()):
                    if expires <= now or idx % 3 == 0:
                        self._cache.pop(key, None)

    def get(self, key):
        try:
            with self._lock.reader():
                expires, value = self._cache[key]
                if expires > time():
                    return pickle.loads(value)
        except (KeyError, pickle.PickleError):
            return None

    def set(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        self._prune()
        new_key = (time() + timeout, pickle.dumps(value,
                                                  pickle.HIGHEST_PROTOCOL))
        with self._lock.writer():
            self._cache[key] = new_key
        return True

    def add(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        self._prune()
        with self._lock.reader():
            if key in self._cache:
                return False
        item = (time() + timeout, pickle.dumps(value,
            pickle.HIGHEST_PROTOCOL))
        with self._lock.writer():
            self._cache.setdefault(key, item)
        return True

    def delete(self, key):
        with self._lock.writer():
            return self._cache.pop(key, None) is not None
