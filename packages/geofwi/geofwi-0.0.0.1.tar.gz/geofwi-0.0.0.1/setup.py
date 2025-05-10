#!/usr/bin/env python
# -*- encoding: utf8 -*-
# import glob
# import inspect
# import io
# import os

from setuptools import setup
import numpy
long_description = """
Source code: https://github.com/aaspip/geofwi""".strip() 


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")).read()

# from numpy.distutils.core import setup 
setup(
    name="geofwi",
    version="0.0.0.1",
    license='MIT License',
    description="GeoFWI: A lightweight velocity model dataset for benchmarking full waveform inversion using deep learning",
    long_description=long_description,
    author="geofwi developing team",
    author_email="chenyk2016@gmail.com",
    url="https://github.com/aaspip/geofwi",
    packages=['geofwi'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License"
    ],
    keywords=[
        "seismology", "seismic imaging", "computational seismology", "AI for science"
    ],
    install_requires=[
        "numpy", "scipy", "matplotlib"
    ],
    extras_require={
        "docs": ["sphinx", "ipython", "runipy"]
    }
)
