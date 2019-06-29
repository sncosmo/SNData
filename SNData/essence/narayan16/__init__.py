#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

# Todo: Add spectroscopic data
"""This module provides access to 213 Type Ia supernovae discovered by the
ESSENCE survey at redshifts 0.1 <= z <= 0.81 between 2002 and 2008. It includes
R and I band photometry measured from images obtained using the MOSAIC II
camera at the CTIO Blanco, along with rapid-response spectroscopy for each
object. Spectroscopic follow-up observations were used to determine an
quantitative classifications and precise redshifts.
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
from ._data_parsing import get_sncosmo_input
from ._data_parsing import iter_data
from ._data_parsing import load_table
from ._data_parsing import register_filters
from ._meta import band_names, lambda_effective

survey_name = 'Equation of State: Supernovae trace Cosmic Expansion'
survey_abbrev = 'ESSENCE'
# Todo: survey_url = 'https://csp.obs.carnegiescience.edu/news-items/csp-dr3-photometry-released'
data_type = 'photometric'
publications = ('Narayan et al. 2016',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2016ApJS..224....3N/abstract'
