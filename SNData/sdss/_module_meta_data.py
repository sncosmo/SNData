#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Download any data files that do not exist locally and define file paths to
the local data for use by the parent module.
"""

import os
from itertools import product

from .._utils import download_data, register_filter

# Define local paths of published SDSS data
_file_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(_file_dir, 'data')
filter_dir = os.path.join(data_dir, 'doi_2010_filters/')  # SDSS filters
snana_dir = os.path.join(data_dir, 'SDSS_dataRelease-snana/')  # SNANA files
master_table_path = os.path.join(data_dir, 'master_data.txt')  # Master table
smp_dir = os.path.join(data_dir, 'SMP_Data/')  # SMP data files
outlier_path = os.path.join(snana_dir,
                            'SDSS_allCandidates+BOSS.IGNORE')  # Outlier data

# Download light curve data if it does not exist locally
_sdss_url = 'https://data.sdss.org/sas/dr10/boss/papers/supernova/'
_local_data_file_names = [master_table_path, smp_dir, snana_dir]
_remote_data_file_names = ['master_data.txt',
                           'SMP_Data.tar.gz',
                           'SDSS_dataRelease-snana.tar.gz']

download_data(
    base_url=_sdss_url,
    out_dir=data_dir,
    remote_name=_remote_data_file_names,
    check_local_name=_local_data_file_names
)

# Download filter profiles if they do not exist locally
_filt_url = 'http://www.ioa.s.u-tokyo.ac.jp/~doi/sdss/'
_local_filt_file_names = [f'{band}{column}.dat' for band, column in
                          product('ugriz', '123456')]

download_data(
    base_url=_filt_url,
    out_dir=filter_dir,
    remote_name=_local_filt_file_names,
    check_local_name=_local_filt_file_names
)

# Register filters if not already registered
# Effective wavelengths for SDSS filters ugriz in angstroms
# are available at https://www.sdss.org/instruments/camera/#Filters
band_names = [f'91bg_proj_sdss_{band}{column}' for band, column in
              product('ugriz', '123456')]

lambda_effective = tuple((3551, 3551, 3551, 3551, 3551, 3551,
                          4686, 4686, 4686, 4686, 4686, 4686,
                          6166, 6166, 6166, 6166, 6166, 6166,
                          7480, 7480, 7480, 7480, 7480, 7480,
                          8932, 8932, 8932, 8932, 8932, 8932))

for _filter_file, _filter_name in zip(_local_filt_file_names, band_names):
    fpath = os.path.join(filter_dir, _filter_file)
    register_filter(fpath, _filter_name)
