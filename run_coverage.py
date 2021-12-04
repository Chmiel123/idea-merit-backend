
import unittest
import coverage
import sys
import os

abspath = os.path.abspath(__file__)
path = os.path.join(os.path.dirname(abspath), 'src')
os.chdir(path)
sys.path.insert(1, path)

COV = coverage.coverage(
    branch=True,
    include='/*',
    omit=[
        '/test/*',
        '../env/*',
        '/usr/*',
        'C:/Program Files/*'
    ]
)
COV.start()

tests = unittest.TestLoader().discover('test', pattern='*_test.py')
result = unittest.TextTestRunner(verbosity=2).run(tests)
if result.wasSuccessful():
    COV.stop()
    COV.save()
    print('Coverage Summary:')
    COV.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, '../tmp/coverage')
    COV.html_report(directory=covdir)
    indexPath = os.path.abspath(covdir + '/index.html')
    print('HTML version: file://%s' % indexPath)
    COV.erase()