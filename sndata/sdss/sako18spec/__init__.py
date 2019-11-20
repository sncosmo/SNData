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

Deviations from the standard UI:
  - This module provides spectroscopic data and as such the ``band_names``,
    and ``lambda_effective`` attributes are not available.

Cuts on returned data:
  - A spectra is included in the data release for object ``15301``, but no
    information about this spectra is provided in the spectra summary table
    (Table 9). This spectra is ignored.
  - Seven spectroscopically observed objects are missing a reported Ra, Dec,
    and redshift. These include: ``13046``, ``13346``, ``15833``, ``17134``,
    ``17135``, ``19819``, and ``6471``.
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
data_type = 'spectroscopic'
publications = ('Sako et al. (2018)',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2018PASP..130f4002S/abstract'
