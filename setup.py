import sys

from setuptools import setup

requirements = ['Click', 'Jinja2', 'tabulate']

if 'win32' in sys.platform.lower():
    # Windows needs colorama for the terminal colors to work.
    requirements.append('colorama')


def get_readme():
    with open('README.rst', encoding='UTF-8') as readme:
        return readme.read()

setup(
    name='EasyEuler',
    version='1.2.0',
    description='A command line tool for Project Euler',
    long_description=get_readme(),
    license='MIT',
    author='Encrylize',
    author_email='encrylize@gmail.com',
    url='https://github.com/Encrylize/EasyEuler',
    keywords=['EasyEuler', 'ProjectEuler', 'euler', 'Project-Euler'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Natural Language :: English'
    ],
    packages=['EasyEuler', 'EasyEuler.commands'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        easyeuler=EasyEuler.cli:cli
    ''',
    include_package_data=True,
    zip_safe=False
)
