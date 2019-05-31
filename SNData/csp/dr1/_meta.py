#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module specifies file meta and urls used by this submodule."""

from pathlib import Path

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

# Define local paths of published data
spectra_dir = data_dir / 'CSP_spectra_DR1'  # DR1 spectra
table_dir = data_dir / 'tables'  # DR3 paper tables

# Define urls for remote data
spectra_url = 'https://csp.obs.carnegiescience.edu/data/CSP_spectra_DR1.tgz'
table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/ApJ/773/53'
