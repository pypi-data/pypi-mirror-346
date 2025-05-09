#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import setuptools
from setuptools import find_packages

NAME = 'model-framework'
PACKAGE = 'mframework'
VERSION = "0.1.0"
AUTHOR = 'Aaron Dettmann'
EMAIL = 'dettmann@kth.se'
DESCRIPTION = 'Framework to build consistent model interfaces'
URL = 'https://github.com/airinnova/model-framework'
REQUIRES_PYTHON = '>=3.11.11'
REQUIRED = [
    'commonlibs',
    'schemadict',
]
README = 'README.rst'
PACKAGE_DIR = 'src/'
LICENSE = 'Apache License 2.0'


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, README), "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    url=URL,
    include_package_data=True,
    package_dir={'': PACKAGE_DIR},
    license=LICENSE,
    # packages=[PACKAGE],
    packages=find_packages(where=PACKAGE_DIR),
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    # See: https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
    ],
)
