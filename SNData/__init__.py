#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to supernova light-curve data from DES, SDSS,
and CSP. Data is downloaded automatically if it is not locally available,
including filter transmission curves. This package will temporarily register
filter transmission curves with SNCosmo using the naming scheme
`SND_<survey name>_<filter name>`.

An example of accessing SDSS data is provided below. The interface for DES or
CSP is the same, except you would import `des` or `csp` instead of `sdss`.

>>> from SNData import sdss
>>>
>>> # Description of data cuts and where the data comes from
>>> help(sdss.master_table)
>>>
>>> # Summary table of SDSS SN data
>>> print(sdss.master_table)
>>>
>>> # Print data about the survey's band-passes
>>> print(sdss.band_names)
>>> print(sdss.lambda_effective)
>>>
>>> # Get SDSS data for a specific object (No data cuts applied)
>>> print(sdss.get_data_for_id(685))
>>>
>>> # Get SNCosmo input table for specific object (Possible data cuts applied)
>>> print(sdss.get_input_for_id(685))
>>>
>>> # Iterable of SNCosmo input tables for each target
>>> for table in sdss.iter_sncosmo_input():
>>>     print(table)
>>>

Any data cuts applied by a given module or function are described in that
module and function's docstring.
"""

from . import csp, des, sdss
