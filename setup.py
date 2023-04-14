#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

pkg_name = "pandas_practice"
here = path.abspath(path.dirname(__file__))

long_description = """None"""

with open(path.join(here, "requirements.txt")) as f:
    requirements = f.read().splitlines()

with open(path.join(here, pkg_name, "version.py")) as f:
    exec(f.read())

setup(
    name="pandas_practice",
    version=__version__,  # noqa: F821
    description="None",
    long_description=long_description,
    author="Chris Brozdowski",
    author_email="cbrozdowski@yahoo.com",
    license="MIT",
    url="https://github.com/cbroz1/pandas_practice",
    keywords="pandas python",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=requirements,
)
