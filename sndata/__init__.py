#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This package provides access to supernova light-curve data from various
surveys.
"""

from . import csp, des, essence, sdss
from ._combine_data import CombinedDataset
from ._integrations import parse_snoopy_data
from ._integrations import query_ned_coords
from ._integrations import query_osc
from ._integrations import query_osc_photometry
from ._integrations import query_osc_spectra

__version__ = '0.5.0'
__author__ = 'Daniel Perrefort'
__license__ = 'MIT'


def delete_all_data():
    """Delete all data downloaded by SNData for all surveys / data releases"""

    modules = (csp.dr3, csp.dr1, des.sn3yr, sdss.sako18, essence.narayan16)
    for module in modules:
        module.delete_module_data()
