#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
from pathlib import Path

from setuptools import find_packages, setup

# Get list of requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Create long description
url = 'https://sn-data.readthedocs.io'
long_description = (
    "SNData provides a Python interface for data releases published by "
    f"various supernova surveys. For more information see {url}"
)

# Get package version
init_path = Path(__file__).resolve().parent / 'sndata/__init__.py'
with open(init_path, 'r') as f:
    s = f.read()

versionRegExp = re.compile("__version__ = '(.*?)'")
__version__ = versionRegExp.findall(s)[0]

setup(name='sndata',
      version=__version__,
      packages=find_packages(),
      keywords='Supernova Astronomy Data Release',
      description='A Python interface for data published by various supernova surveys',
      long_description=long_description,
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
      url=url,
      license='GPL v3',

      python_requires='>=3.6',
      install_requires=requirements,

      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      include_package_data=False)
