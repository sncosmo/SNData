#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module specifies file meta and urls used by this submodule."""

from pathlib import Path

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

# Define local paths of published data
master_table_path = data_dir / 'master_data.txt'  # Master table
spectra_dir = data_dir / 'Spectra_txt'  # spectra txt files
spectra_zip = _file_dir / 'Spectra_txt.zip'  # Compressed spectra files
photometry_master_table_path = data_dir / 'phot_master'  # Master table from photometric release

# Define urls for remote data
master_table_url = 'https://data.sdss.org/sas/dr10/boss/papers/supernova/spectroscopy_table.txt'
photometry_master_table_url = 'https://data.sdss.org/sas/dr10/boss/papers/supernova/master_data.txt'
spectra_url = 'https://data.sdss.org/sas/dr10/boss/papers/supernova/Spectra.tar.gz'
