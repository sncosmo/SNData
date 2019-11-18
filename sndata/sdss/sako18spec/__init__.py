# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to the **spectroscopic** data release of the
Sloan Digital Sky Survey-II (SDSS-II) Supernova Survey conducted between 2005
and 2007. Light curves are presented for 10,258 variable and transient sources
discovered through repeat ugriz imaging of SDSS Stripe 82, a 300 deg2 area
along the celestial equator. This data release is comprised of all transient
sources brighter than r ≃ 22.5 mag with no history of variability prior to
2004. (Source: Sako et al. 2018)

For the photometric data of this data release see the ``sako18`` module.

.. note::
   In the returned data tables, the ``extraction`` column refers to the type
   extraction performed on the spectrum. The ``type`` column refers to the
   actual type of the spectrum determined after the recorded spectra were
   inspected. In some cases the galaxy contribution dominates the observation
   and there was no discernible SN light. Thus there may be cases where the
   extraction of a SN spectra was attempted, but the resulting spectrum was
   galactic in type.

Deviations from the standard UI:
  - This module provides spectroscopic data and as such the ``band_names``,
    and ``lambda_effective`` attributes are not available.

Cuts on returned data:
  - None
"""

from ..sako18._data_download import delete_module_data
from ..sako18._data_download import download_module_data
from ._data_parsing import get_available_ids
from ._data_parsing import get_available_tables
from ._data_parsing import get_data_for_id
from ._data_parsing import iter_data
from ._data_parsing import load_table
from ._data_parsing import register_filters

survey_name = 'Sloan Digital Sky Survey'
survey_abbrev = 'SDSS'
release = 'sako18'
survey_url = 'https://portal.nersc.gov/project/dessn/SDSS/dataRelease/'
data_type = 'spectroscopy'
publications = ('Sako et al. (2018)',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2018PASP..130f4002S/abstract'
