#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This package provides access to supernova light-curve data from various
surveys.
"""

from . import csp, des, sdss
from ._integrations import parse_snoopy_data
from ._integrations import query_ned_coords
from ._integrations import query_osc
from ._integrations import query_osc_photometry
from ._integrations import query_osc_spectra

__version__ = '0.0.9'
__author__ = 'Daniel Perrefort'
