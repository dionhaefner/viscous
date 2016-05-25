#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

def viscous_scripts():
    return [""]

setup(name='viscous',
      version='0.1',
      description="Multipurpose utilities for post-processing of CESM POP2 data of low-viscosity runs",
      author='Dion Häfner <mail@dionhaefner.de>',
      author_email='mail@dionhaefner.de',
      url='',
      packages = find_packages(),
      install_requires=['numpy','scipy','matplotlib','seaborn','ipython'],
     # scripts=viscous_scripts()
      )
