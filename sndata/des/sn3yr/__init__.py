#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to data from the first public data release of
the Dark Energy Survey Supernova Program, DES-SN3YR. It includes griz light
curves of 251 supernovae from the first 3 years of the Dark Energy Survey
Supernova Program’s (DES-SN) spectroscopically classified sample.
(Source: Brout et al. 2019)

Deviations from the standard UI:
  - None

Cuts on returned data:
  - None
"""

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
release = 'sn3yr'
survey_url = 'https://des.ncsa.illinois.edu/'
data_type = 'photometry'
publications = (
    'Burke et al. 2017',
    'Brout et al. 2019',
    'Brout et al. 2018-SYS'
)

ads_url = 'https://ui.adsabs.harvard.edu/abs/2019ApJ...874..106B/abstract'
