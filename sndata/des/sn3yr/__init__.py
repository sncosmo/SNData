#!/usr/bin/env python3
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
from ._meta import (
    ads_url,
    band_names,
    data_type,
    lambda_effective,
    publications,
    release,
    survey_abbrev,
    survey_name,
    survey_url
)
