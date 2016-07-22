import os
import unittest

import coverage

tests = unittest.TestLoader().discover('tests')
cov = coverage.coverage(branch=True, include='EasyEuler/*.py')
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
COVERAGE_PATH = os.path.join(BASE_PATH, 'tmp/coverage')

cov.start()
unittest.TextTestRunner(verbosity=2).run(tests)
cov.stop()
cov.save()

print('Coverage Summary:')
cov.report()
cov.html_report(directory=COVERAGE_PATH)
print('HTML version: %s/index.html' % COVERAGE_PATH)
cov.erase()
