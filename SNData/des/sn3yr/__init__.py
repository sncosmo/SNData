#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to data from the first public data release of
the Dark Energy Survey Supernova Program, DES-SN3YR.
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

survey_name = 'Dark Energy Survey'
survey_abbrev = 'DES'
data_type = 'photometry'
publication = 'Brout et al. (2019)'
ads = 'https://ui.adsabs.harvard.edu/abs/2019ApJ...874..106B/abstract'
