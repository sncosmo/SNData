#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides access to photometric data for 213 Type Ia supernovae
discovered by the ESSENCE survey at redshifts 0.1 <= z <= 0.81 between 2002 and
2008. It includes R and I band photometry measured from images obtained using
the MOSAIC II camera at the CTIO Blanco telescope.
(Source: Narayan et al. 2017)

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
