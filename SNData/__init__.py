#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This package provides access to supernova light-curve data from various
surveys.
"""

from . import csp, des, sdss
from ._utils import parse_snoopy_data, query_ned_coords
from  ._osc import query_osc_photometry, query_osc_spectra

__version__ = '0.0.8'
__author__ = 'Daniel Perrefort'
