"""Runs the unit tests without test coverage."""

import unittest


tests = unittest.TestLoader().discover('test', pattern='*_test.py')
result = unittest.TextTestRunner(verbosity=2).run(tests)
