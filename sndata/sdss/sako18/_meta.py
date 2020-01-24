#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module specifies file meta and urls used by this submodule."""

from itertools import product
from pathlib import Path
from urllib.parse import urljoin

import numpy as np

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

# Define local paths of downloaded data
filter_dir = data_dir / 'doi_2010_filters/'  # Transmission filters
table_dir = data_dir / 'tables/'  # Tables from the published paper
smp_dir = data_dir / 'SMP_Data/'  # SMP data files (photometric light-curves)
snana_dir = data_dir / 'SDSS_dataRelease-snana/'  # SNANA files including list of outliers
outlier_path = snana_dir / 'SDSS_allCandidates+BOSS/SDSS_allCandidates+BOSS.IGNORE'  # Outlier data
spectra_dir = data_dir / 'Spectra_txt'  # spectra files
spectra_zip = _file_dir / 'Spectra_txt.zip'  # compressed spectra files

# Define urls and file names for remote data
filter_url = 'http://www.ioa.s.u-tokyo.ac.jp/~doi/sdss/'

base_url = 'https://portal.nersc.gov/project/dessn/SDSS/dataRelease/'
table_names = 'master_data.txt', 'Table2.txt', 'Table9.txt', 'Table11.txt', 'Table12.txt'
smp_url = urljoin(base_url, 'SMP_Data.tar.gz')
snana_url = urljoin(base_url, 'SDSS_dataRelease-snana.tar.gz')
spectra_url = urljoin(base_url, 'Spectra.tar.gz')

# Filter information
# Effective wavelengths for SDSS filters ugriz in angstroms
# are available at https://www.sdss.org/instruments/camera/#Filters
band_names = tuple(f'sdss_sako18_{b}{c}' for b, c in product('ugriz', '123456'))
filter_file_names = tuple(f'{b}{c}.dat' for b, c in product('ugriz', '123456'))
zero_point = [2.5 * np.log10(3631) for _ in band_names]
lambda_effective = (
    3551, 3551, 3551, 3551, 3551, 3551,
    4686, 4686, 4686, 4686, 4686, 4686,
    6166, 6166, 6166, 6166, 6166, 6166,
    7480, 7480, 7480, 7480, 7480, 7480,
    8932, 8932, 8932, 8932, 8932, 8932
)
