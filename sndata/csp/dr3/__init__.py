#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides access to data from the third data release of the
Carnegie Supernova Project (CSP) which includes natural-system optical (ugriBV)
and near-infrared (YJH) photometry of 134 supernovae (SNe) that were observed
in 2004-2009 as part of the first stage of the Carnegie Supernova Project
(CSP-I). The sample consists of 123 Type Ia SNe, 5 Type Iax SNe,
2 super-Chandrasekhar SN candidates, 2 Type Ia SNe interacting with
circumstellar matter, and 2 SN 2006bt-like events. The redshifts of the
objects range from z=0.0037 to 0.0835; the median redshift is 0.0241. For 120
(90%) of these SNe, near-infrared photometry was obtained.
(Source: Krisciunas et al. 2017)

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
