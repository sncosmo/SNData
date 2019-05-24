# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to data from the SDSS-II SN Catalog Data
Release, published in Sako et al. 2014.
"""

from itertools import product as _product

from . import _paths
from ._data_download import delete_module_data
from ._data_download import download_module_data
from ._data_parsing import get_data_for_id
from ._data_parsing import get_input_for_id
from ._data_parsing import iter_sncosmo_input
from ... import _utils

# Effective wavelengths for SDSS filters ugriz in angstroms
# are available at https://www.sdss.org/instruments/camera/#Filters
band_names = [f'SND_sdss_{band}{column}' for band, column in
              _product('ugriz', '123456')]

lambda_effective = tuple((3551, 3551, 3551, 3551, 3551, 3551,
                          4686, 4686, 4686, 4686, 4686, 4686,
                          6166, 6166, 6166, 6166, 6166, 6166,
                          7480, 7480, 7480, 7480, 7480, 7480,
                          8932, 8932, 8932, 8932, 8932, 8932))

for _file_name, _band_name in zip(_paths.filter_file_names, band_names):
    fpath = _paths.filter_dir / _file_name
    _utils.register_filter(fpath, _band_name)
