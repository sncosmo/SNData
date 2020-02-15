#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This file specifies file meta and urls used by the parent module."""

import os
from pathlib import Path

from ... import _utils as utils

# General metadata
survey_name = 'Carnegie Supernova Project'
survey_abbrev = 'CSP'
release = 'dr1'
survey_url = 'https://csp.obs.carnegiescience.edu/news-items/CSP_spectra_DR1'
data_type = 'spectroscopic'
publications = ('Folatelli et al. 2013',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2013ApJ...773...53F/abstract'

if 'SNDATA_DIR' in os.environ:
    data_dir = utils.create_data_dir(survey_name, release)

else:
    data_dir = Path(__file__).resolve().parent / 'data'

# Define local paths of published data
spectra_dir = data_dir / 'CSP_spectra_DR1'  # DR1 spectra
table_dir = data_dir / 'tables'  # DR3 paper tables

# Define urls for remote data
spectra_url = 'https://csp.obs.carnegiescience.edu/data/CSP_spectra_DR1.tgz'
table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/ApJ/773/53'
