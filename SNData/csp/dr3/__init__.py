#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to data from the third data release of the
Carnegie Supernova Project (CSP).
"""

from ._data_download import delete_module_data
from ._data_download import download_module_data
from ._data_parsing import get_data_for_id
from ._data_parsing import get_input_for_id
from ._data_parsing import iter_sncosmo_input
from ._data_parsing import load_table
from ._meta import band_names
from ._meta import lambda_effective
from ._meta import zero_point
