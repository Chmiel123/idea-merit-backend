"""Runs the unit tests without test coverage."""

import unittest
import sys
import os

abspath = os.path.abspath(__file__)
path = os.path.dirname(abspath) + '\\src'
os.chdir(path)
sys.path.insert(1, path)

pattern = ''
if len(sys.argv) > 1:
    pattern = sys.argv[1]
pattern = f'*{pattern}*_test.py'

print (f'pattern: {pattern}')
tests = unittest.TestLoader().discover('test/', pattern=pattern)
result = unittest.TextTestRunner(verbosity=2).run(tests)
