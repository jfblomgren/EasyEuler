import sys

from setuptools import setup


requirements = ['Click', 'Jinja2']

if 'win32' in sys.platform.lower():
    # Windows needs colorama for the terminal colors to work.
    requirements.append('colorama')


def get_readme():
    with open('README.rst') as readme:
        return readme.read()

setup(
    name='EasyEuler',
    packages=['EasyEuler', 'EasyEuler.commands'],
    version='0.9.1',
    description='A command line tool for Project Euler',
    long_description=get_readme(),
    author='Encrylize',
    author_email='encrylize@gmail.com',
    url='https://github.com/Encrylize/EasyEuler',
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        easyeuler=EasyEuler.cli:cli
    ''',
    keywords=['EasyEuler', 'ProjectEuler', 'euler', 'Project-Euler'],
    include_package_data=True,
    zip_safe=False
)
