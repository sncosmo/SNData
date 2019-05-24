# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to data from the SDSS-II SN Catalog Data
Release, published in Sako et al. 2014.
"""

from ._data_download import delete_module_data
from ._data_download import download_module_data
from ._data_parsing import get_data_for_id
from ._data_parsing import get_input_for_id
from ._data_parsing import iter_sncosmo_input
from ._data_parsing import load_table
from ._meta import band_names
from ._meta import lambda_effective
# Todo: from ._meta import zero_point
