import io
import os
from os.path import join, dirname

import dpm
from setuptools import setup, find_packages


def read(*paths):
    """Read a text file."""
    fullpath = join(dirname(__file__), *paths)
    return io.open(fullpath, encoding='utf-8').read().strip()


INSTALL_REQUIRES = [
    'click',
    'configobj',
    'datapackage',
    'requests',
    'six'
]

TESTS_REQUIRE = [
    'nose',
    'mock',
    'mocket',
    'responses'
]


setup(
    name='dpmpy',
    version=dpm.__version__,
    description='dpmpy is a package manager for datapackages',
    long_description=read('README.md'),
    author='Atomatic',
    author_email='hello@atomatic.net',
    url='https://github.com/frictionlessdata/dpmpy',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require={'develop': TESTS_REQUIRE},
    test_suite='nose.collector',
    entry_points={
        'console_scripts': ['dpmpy = dpm.main:cli'],
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Android',
        'Programming Language :: C',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)
