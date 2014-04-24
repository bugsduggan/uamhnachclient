#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name             = 'uamhnachclient',
    version          = '0.1',

    author           = 'Tom Leaman',
    author_email     = 'tom@tomleaman.co.uk',
    url              = 'https://github.com/bugsduggan/uamhnachclient',

    description      = 'A client for Uamhnach',
    long_description = open('README.md').read(),

    packages         = find_packages(),
    install_requires = ['requests==2.2.1', 'wsgiref==0.1.2'],
    tests_require    = [],

    entry_points     = {
        'console_scripts': [
            'uamhnach  = uamhnachclient:main',
        ]
    },

    classifiers     = [
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
