#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to spectroscopic observations from the ESSENCE
high-redshift supernova (SN) survey during its first two years of operation.
It includes spectra of 52 Type Ia supernovae (SNe Ia) at moderate redshifts
(0.2 <= z<= 0.8). (Source: Foley et al. 2009)

Deviations from the standard UI:
  - This module provides spectroscopic data and does not support integration
    features with SNCosmo
  - The ``band_names``, ``lambda_effective``, and ``register_filter``
    attributes are not available.

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

survey_name = 'Equation of State: Supernovae trace Cosmic Expansion'
survey_abbrev = 'ESSENCE'
release = 'matheson05'
survey_url = 'http://www.ctio.noao.edu/essence/'
data_type = 'spectroscopic'
publications = ('Matheson et al. 2005',)
ads_url = 'https://ui.adsabs.harvard.edu/#abs/2005AJ....129.2352M'
