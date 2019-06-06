# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to data from the SDSS-II SN Catalog Data
Release, published in Sako et al. 2018.
"""

from ._data_download import data_is_available
from ._data_download import delete_module_data
from ._data_download import download_module_data
from ._data_parsing import get_available_ids
from ._data_parsing import get_available_tables
from ._data_parsing import get_data_for_id
from ._data_parsing import iter_data
from ._data_parsing import load_table
from ._data_parsing import register_filters
from ._meta import band_names, lambda_effective

survey_name = 'Sloan Digital Sky Survey'
survey_abbrev = 'SDSS'
data_type = 'photometry'
publication = 'Sako et al. (2018)'
ads = 'https://ui.adsabs.harvard.edu/abs/2018PASP..130f4002S/abstract'
