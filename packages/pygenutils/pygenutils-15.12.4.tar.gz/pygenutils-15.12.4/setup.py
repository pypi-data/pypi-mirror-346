#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**
Run this program to make of the entire module, repository, installable.

Created: {CREATION_DATE}
Current Version: 15.12.4
"""

#----------------#
# Import modules #
#----------------#

from setuptools import setup, find_packages
from datetime import datetime as dt

#-------------------#
# Define parameters #
#-------------------#

TIME_FMT_STR = "%Y-%m-%d %H:%M:%S"
CREATION_DATE = dt.now().strftime(TIME_FMT_STR)
PACKAGE_NAME = "pygenutils"

#--------------------------------#
# Define the metadata dictionary #
#--------------------------------#

METADATA_DICT = dict(
    name=PACKAGE_NAME,
    version="15.12.4",
    description="A comprehensive Python utility library for general-purpose and specialised tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jon Ander Gabantxo",
    author_email="jagabantxo@gmail.com",
    url="https://github.com/EusDancerDev/pygenutils",
    packages=find_packages(where=".", include=["pygenutils*"], exclude=["tests*", "tests.*", "*.tests", "*.tests.*"]),
    python_requires=">=3.9",
    install_requires=[
        "more_itertools>=10.0.0",
        "numpy>=1.21.0,<2.0.0",
        "pandas>=1.3.0,<2.0.0",
        "filewise>=3.7.0",
        "paramlib>=3.4.0",
        "arrow>=1.2.0",
    ],
    extras_require={
        "xarray": ["xarray>=0.20.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
    },
    package_data={
        "pygenutils": ["*.yaml", "*.json"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    project_urls={
        "Homepage": "https://github.com/EusDancerDev/pygenutils",
        "Documentation": "https://github.com/EusDancerDev/pygenutils#readme",
        "Repository": "https://github.com/EusDancerDev/pygenutils.git",
        "Bug Reports": "https://github.com/EusDancerDev/pygenutils/issues",
    },
)

# Pass it to the 'setup' module #
setup(**METADATA_DICT)
