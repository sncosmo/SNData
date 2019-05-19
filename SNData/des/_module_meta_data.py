#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Download any data files that do not exist locally and define file paths to
the local data for use by the parent module.
"""

import os

from .._utils import download_data

# Define local paths of published DES data
_file_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(_file_dir, 'data')
filter_dir = os.path.join(data_dir, '01-FILTERS')
photometry_dir = os.path.join(data_dir, '02-DATA_PHOTOMETRY/DES-SN3YR_DES')
fits_dir = os.path.join(data_dir, '04-BBCFITS')
master_table_path = os.path.join(fits_dir, 'SALT2mu_DES+LOWZ_C11.FITRES')

# Download data if it does not exist
_des_url = 'http://desdr-server.ncsa.illinois.edu/despublic/sn_files/y3/tar_files/'
_local_file_names = [filter_dir, photometry_dir, fits_dir]
_remote_file_names = ['01-FILTERS.tar.gz',
                      '02-DATA_PHOTOMETRY.tar.gz',
                      '04-BBCFITS.tar.gz']

download_data(
    base_url=_des_url,
    out_dir=data_dir,
    remote_name=_remote_file_names,
    check_local_name=_local_file_names)

# Effective wavelengths taken from
# http://www.mso.anu.edu.au/~brad/filters.html
band_names = ('desg', 'desr', 'desi', 'desz', 'desy')
lambda_effective = (5270, 6590, 7890, 9760, 10030)

# Todo: Register filter profiles
