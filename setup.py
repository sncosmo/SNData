#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='SNData',
      version='0.0.1',
      packages=['SNData'],
      keywords='Supernova Astronomy Data Release',
      description='Models the atmospheric transmission function for KPNO',
      long_description="",  # Todo
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics'
      ],

      author='Daniel Perrefort',
      author_email='djperrefort@pitt.edu',
      # url=, Todo
      license='GPL v3',

      python_requires='>=2.6',
      install_requires=requirements,

      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      include_package_data=False)
