# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to the data release of the Sloan Digital Sky
Survey-II (SDSS-II) Supernova Survey conducted between 2005 and 2007. Light
curves are presented for 10,258 variable and transient sources discovered
through repeat ugriz imaging of SDSS Stripe 82, a 300 deg2 area along the
celestial equator. This data release is comprised of all transient sources
brighter than r ≃ 22.5 mag with no history of variability prior to 2004.
(Source: Sako et al. 2018)

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
from ._meta import band_names, lambda_effective

survey_name = 'Sloan Digital Sky Survey'
survey_abbrev = 'SDSS'
release = 'sako18'
survey_url = 'http://data.darkenergysurvey.org/sdsssn/dataRelease/'
data_type = 'photometry'
publications = ('Sako et al. (2018)',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2018PASP..130f4002S/abstract'
