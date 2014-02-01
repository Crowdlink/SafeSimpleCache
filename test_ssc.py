import unittest
# import werkzeugs test suite maker for caches
from werkzeug.testsuite.contrib.cache import CacheTestCase
from flask_ssc import SafeSimpleCache


class SafeSimpleCacheTestCase(CacheTestCase):
    make_cache = SafeSimpleCache


class SafeSimpleCacheTestCaseNopickle(CacheTestCase):
    def make_cache(self):
        return SafeSimpleCache(pickle=False)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SafeSimpleCacheTestCase))
    suite.addTest(unittest.makeSuite(SafeSimpleCacheTestCaseNopickle))
    unittest.TextTestRunner(verbosity=2).run(suite)
