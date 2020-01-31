# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""The ``betoule14`` module provides access to light-curves used in a joint
analysis of type Ia supernova (SN Ia) observations obtained by the SDSS-II
and SNLS collaborations. The data set includes several low-redshift samples
(z<0.1), all 3 seasons from the SDSS-II (0.05 < z < 0.4), and 3 years from
SNLS (0.2 <z < 1) and totals 740 spectroscopically confirmed type Ia
supernovae with high quality light curves. (Source: Betoule et al. 2014)

This data set includes observations taken in the pre 2015 MegaCam filter set
used by the Canada-France-Hawaii Telescope (CFHT). These filters were measured
at multiple positions by both the observing team and manufacturer. Transmission
functions registered by this module represent the average transmission across
the filter as reported by the manufacturer.

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
