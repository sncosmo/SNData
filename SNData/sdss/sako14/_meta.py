#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module specifies file meta and urls used by this submodule."""

from itertools import product
from pathlib import Path

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

# Define local paths of published data
filter_dir = data_dir / 'doi_2010_filters/'
snana_dir = data_dir / 'SDSS_dataRelease-snana/'  # SNANA files
master_table_path = data_dir / 'master_data.txt'  # Master table
smp_dir = data_dir / 'SMP_Data/'  # SMP data files
outlier_path = snana_dir / 'SDSS_allCandidates+BOSS.IGNORE'  # Outlier data
table_dir = data_dir / 'tables'  # Sako paper tables

# Define urls for remote data
filter_url = 'http://www.ioa.s.u-tokyo.ac.jp/~doi/sdss/'
sdss_url = 'https://data.sdss.org/sas/dr10/boss/papers/supernova/'

# Filter information
# Effective wavelengths for SDSS filters ugriz in angstroms
# are available at https://www.sdss.org/instruments/camera/#Filters
band_names = \
    [f'SND_sdss_{band}{column}' for band, column in product('ugriz', '123456')]

filter_file_names = \
    [f'{band}{column}.dat' for band, column in product('ugriz', '123456')]

lambda_effective = tuple((3551, 3551, 3551, 3551, 3551, 3551,
                          4686, 4686, 4686, 4686, 4686, 4686,
                          6166, 6166, 6166, 6166, 6166, 6166,
                          7480, 7480, 7480, 7480, 7480, 7480,
                          8932, 8932, 8932, 8932, 8932, 8932))
