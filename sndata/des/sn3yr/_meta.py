#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Download any data files that do not exist locally and define file paths to
the local data for use by the parent module.
"""

from pathlib import Path

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

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

lambda_effective = (5270, 6590, 7890, 9760, 10030)
