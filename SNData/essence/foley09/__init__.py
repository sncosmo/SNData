#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to spectroscopic observations from the ESSENCE
high-redshift supernova (SN) survey during its first four years of operation.
The sample represents 273 hr of spectroscopic observations with 6.5-10 m class
telescopes of objects detected and selected for spectroscopy by the ESSENCE
team. It includes 184 spectra of 156 objects. (Source: Foley et al. 2009)

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
survey_url = 'http://www.ctio.noao.edu/essence/'
data_type = 'spectroscopic'
publications = ('Foley et al. 2009',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2009AJ....137.3731F/abstract'
