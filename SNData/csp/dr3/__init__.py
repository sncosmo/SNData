#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to data from the third data release of the
Carnegie Supernova Project (CSP).
"""

from . import _paths
from ._data_download import delete_module_data
from ._data_download import download_module_data
from ._data_parsing import get_data_for_id
from ._data_parsing import get_input_for_id
from ._data_parsing import iter_sncosmo_input
from ._data_parsing import load_table
from ... import _utils

# Filter information
_band_names = (
    'u', 'g', 'r', 'i', 'B', 'V0', 'V1',
    'V', 'Y', 'H', 'J', 'Jrc2', 'Ydw', 'Jdw', 'Hdw'
)

band_names = [f'SND_csp_{f}' for f in _band_names]
lambda_effective = [
    3639.3, 4765.1, 6223.3, 7609.2, 4350.6, 5369.6, 5401.4,
    5375.2, 10350.8, 12386.5, 12356.3, 16297.7, 10439.8,
    12383.2, 16282.8
]

zero_point = [
    12.986, 15.111, 14.902, 14.545, 14.328, 14.437, 14.393, 14.439,
    13.921, 13.836, 13.836, 13.510, 13.770, 13.866, 13.502
]

# Register filters
for _file_name, _band_name in zip(_paths.filter_file_names, band_names):
    fpath = _paths.filter_dir / _file_name
    _utils.register_filter(fpath, _band_name)
