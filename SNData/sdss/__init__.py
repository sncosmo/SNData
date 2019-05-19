#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to data from the SDSS-II SN Catalog Data
Release. Light curve data is provided from Sako et. al 2018. The master_table
object provides data from Table 1 of the same paper.

Data cuts are applied when calling the `iter_sncosmo_input`
function. They include and are limited to:

1. SDSS observations flagged in the data release as outlier points
2. SDSS observations with a photometric quality flag >= 1024
     (As applied in the data release paper)

For more information on SDSS data products, see:
    https://data.sdss.org/sas/dr10/boss/papers/supernova/
"""

from ._data_access_funcs import get_data_for_id
from ._data_access_funcs import get_input_for_id
from ._data_access_funcs import iter_sncosmo_input
from ._data_access_funcs import master_table
from ._module_meta_data import band_names
from ._module_meta_data import lambda_effective

survey_name = 'SDSS'
