#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This file specifies file meta and urls used by the parent module."""

import os
from pathlib import Path

from ... import _utils as utils

# General metadata
survey_name = 'Dark Energy Survey'
survey_abbrev = 'DES'
release = 'sn3yr'
survey_url = 'https://des.ncsa.illinois.edu/'
data_type = 'photometric'
publications = (
    'Burke et al. 2017',
    'Brout et al. 2019',
    'Brout et al. 2018-SYS'
)

ads_url = 'https://ui.adsabs.harvard.edu/abs/2019ApJ...874..106B/abstract'

if 'SNDATA_DIR' in os.environ:
    data_dir = utils.create_data_dir(survey_name, release)

else:
    data_dir = Path(__file__).resolve().parent / 'data'

# Define local paths of published data
filter_dir = data_dir / '01-FILTERS' / 'DECam'
photometry_dir = data_dir / '02-DATA_PHOTOMETRY/DES-SN3YR_DES'
fits_dir = data_dir / '04-BBCFITS'

# Define urls for remote data
_des_url = 'http://desdr-server.ncsa.illinois.edu/despublic/sn_files/y3/tar_files/'
filter_url = _des_url + '01-FILTERS.tar.gz'
photometry_url = _des_url + '02-DATA_PHOTOMETRY.tar.gz'
fits_url = _des_url + '04-BBCFITS.tar.gz'

filter_file_names = (
    'DECam_g.dat',
    'DECam_r.dat',
    'DECam_i.dat',
    'DECam_z.dat',
    'DECam_Y.dat')

band_names = (
    'des_sn3yr_g',
    'des_sn3yr_r',
    'des_sn3yr_i',
    'des_sn3yr_z',
    'des_sn3yr_y')

zero_point = tuple(27.5 for _ in band_names)
lambda_effective = (5270, 6590, 7890, 9760, 10030)
