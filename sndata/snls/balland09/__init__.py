#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides access to to the three year data release of the
Supernova Legacy Survey (SNLS) performed by The Canada-France-Hawaï Telescope
(CFHT). It includes 139 spectra of 124 Type Ia supernovae that range from
z = 0.149 to z = 1.031 and have an average redshift of z = 0.63 +/- 0.02.
(Source: Balland et al. 2009)


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
    data_type,
    publications,
    release,
    survey_abbrev,
    survey_name,
    survey_url
)
