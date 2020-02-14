#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This file specifies file meta and urls used by the parent module."""

import os
from pathlib import Path

from ... import _utils as utils

# General metadata
survey_name = 'Supernova Legacy Survey'
survey_abbrev = 'SNLS'
release = 'balland09'
survey_url = 'http://supernovae.in2p3.fr/~balland/VltRelease/'
data_type = 'spectroscopic'
publications = ('Balland et al. 2009',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2009A%26A...507...85B/abstract'

if 'SNDATA_DIR' in os.environ:
    data_dir = utils.create_data_dir(survey_name, release)

else:
    data_dir = Path(__file__).resolve().parent / 'data'

# Define local paths of published data
spectra_dir = data_dir / 'spectra'  # DR1 spectra
table_dir = data_dir / 'tables'  # DR3 paper tables

# Define urls for remote data
phase_spectra_url = 'http://supernovae.in2p3.fr/~balland/VltRelease/PHASE_spec_Balland09.tar.gz'
snonly_spectra_url = 'http://supernovae.in2p3.fr/~balland/VltRelease/snonly_spec_Balland09.tar.gz'
table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/A+A/507/85'
