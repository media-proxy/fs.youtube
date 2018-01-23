#!/usr/bin/env python
# coding: utf-8

with open('README.rst', 'rt') as f:
    DESCRIPTION = f.read()

from setuptools import setup
setup(long_description=DESCRIPTION)
