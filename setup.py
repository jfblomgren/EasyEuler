import sys

from setuptools import setup


requirements = ['Click', 'Jinja2']

if 'win32' in sys.platform.lower():
    # Windows needs colorama for the terminal colors to work.
    requirements.append('colorama')

setup(
    name='EasyEuler',
    version='0.1',
    py_modules=['EasyEuler'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        easyeuler=EasyEuler.cli:cli
    '''
)
