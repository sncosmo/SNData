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

.. important::
    The ``master`` summary table (i.e. ``load_table('master')``) contains
    entries which do not match the available data. This includes 105 entries
    where the object type is listed as “Gal” but the file type is listed
    as “SN” - the meaning of which is unclear. The file names for most of
    these observations have a "sn" prefix, indicating they are in fact SNe
    observations. However, for 16 of these entries the only fits
    file available matching the object and spectrum Ids has the prefix “gal”.
    When returning observational data, we use the file name prefix to determine
    the spectral type ("sn" indicating target observations and "gal"
    indicating host observations.)

Deviations from the standard UI:
  - This module provides spectroscopic data and as such the ``band_names``,
    and ``lambda_effective`` attributes are not available.

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

survey_name = 'Sloan Digital Sky Survey'
survey_abbrev = 'SDSS'
release = 'sako18'
survey_url = 'http://data.darkenergysurvey.org/sdsssn/dataRelease/'
data_type = 'spectroscopy'
publications = ('Sako et al. (2018)',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2018PASP..130f4002S/abstract'
