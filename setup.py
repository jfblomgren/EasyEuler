from setuptools import setup

setup(
    name='EasyEuler',
    version='0.1',
    py_modules=['EasyEuler'],
    install_requires=[
        'Click',
        'Jinja2'
    ],
    entry_points='''
        [console_scripts]
        easyeuler=EasyEuler.cli:cli
    '''
)
