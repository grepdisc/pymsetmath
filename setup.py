try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pymsetmath

setup(
    name="pymsetmath",
    author="Hy Carrinski",
    author_email="hcarrinski@gmail.com",
    url="http://github.com/grepdisc/pymsetmath",
    version="0.1"
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Distributed Computing",
    ],
    description=("Combinatorics with multisets in Python - with applications",
        "to calculations regarding MapReduce results."),
    keywords=["probability partition multiset multinomial"],
    license="MIT",
    long_description=open("README.rst").read(),
    packages=["pymsetmath"],
    provides=["pymsetmath"],
)
