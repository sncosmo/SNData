# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to the **photometric** data release of the Sloan
Digital Sky Survey-II (SDSS-II) Supernova Survey conducted between 2005 and
2007. Light curves are presented for 10,258 variable and transient sources
discovered through repeat ugriz imaging of SDSS Stripe 82, a 300 deg2 area
along the celestial equator. This data release is comprised of all transient
sources brighter than r ≃ 22.5 mag with no history of variability prior to
2004. (Source: Sako et al. 2018)

For the spectroscopic data of this data release see the ``sako18spec`` module.

Deviations from the standard UI:
  - None

Cuts on returned data:
  - Data points manually marked as outliers by the SDSS research time are not
    included in returned data tables.
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
