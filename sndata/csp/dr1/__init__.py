#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides access to spectra from the first release of optical
spectroscopic data of low-redshift Type Ia supernovae (SNe Ia) by the Carnegie
Supernova Project. It includes 604 previously unpublished spectra of 93 SNe Ia.
The observations cover a range of phases from 12 days before to over 150 days
after the time of B-band maximum light. (Source: Folatelli et al. 2013)

Deviations from the standard UI:
  - This module provides spectroscopic data and as such the ``band_names``,
    and ``lambda_effective`` attributes are not available.

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
