#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to spectra from the first release of optical
spectroscopic data of low-redshift Type Ia supernovae (SNe Ia) by the Carnegie
Supernova Project. It includes 604 previously unpublished spectra of 93 SNe Ia.
The observations cover a range of phases from 12 days before to over 150 days
after the time of B-band maximum light. (Source: Folatelli et al. 2013)

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

survey_name = 'Carnegie Supernova Project'
survey_abbrev = 'CSP'
release = 'dr1'
survey_url = 'https://csp.obs.carnegiescience.edu/news-items/CSP_spectra_DR1'
data_type = 'spectroscopic'
publications = ('Folatelli et al. 2013',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2013ApJ...773...53F/abstract'
