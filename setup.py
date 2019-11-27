# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:54:12 2019

@author: Ludovic.SPAETH
"""

import setuptools

with open("README.md","r") as fh: 
    
    long_description = fh.read()
    
setuptools.setup(
    name="electroPyy",
    version="0.0.3",
    author="Ludovic Spaeth",
    author_email="ludovic.spaeth@gmail.com",
    description="Data analysis package for cerebellar fellas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ludo67100/electroPyy_Dev",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: None",
        "Operating System :: OS Independent",
    ]
)    