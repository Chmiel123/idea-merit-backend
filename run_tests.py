"""Runs the unit tests without test coverage."""

import unittest
import sys

pattern = ''
if len(sys.argv) > 1:
    pattern = sys.argv[1]
pattern = f'*{pattern}*_test.py'

print (f'pattern: {pattern}')
tests = unittest.TestLoader().discover('test/', pattern=pattern)
result = unittest.TextTestRunner(verbosity=2).run(tests)
