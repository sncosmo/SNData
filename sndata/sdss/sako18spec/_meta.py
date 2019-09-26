#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module specifies file meta and urls used by this submodule."""

from pathlib import Path

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

# Define local paths of published data
master_table_path = data_dir / 'master_data.txt'  # Master table
spectra_dir = data_dir / 'spectra'  # spetra fits files

# Define urls for remote data
master_table_url = 'https://data.sdss.org/sas/dr10/boss/papers/supernova/spectroscopy_table.txt'
spectra_url = 'https://data.sdss.org/sas/dr10/boss/papers/supernova/Spectra.tar.gz'
