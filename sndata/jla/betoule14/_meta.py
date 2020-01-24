#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module specifies file meta and urls used by this submodule."""

from pathlib import Path

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

# Define local paths of published data
photometry_dir = data_dir / 'jla_light_curves'  # Photometry data
filter_dir = data_dir / 'filters'  # Filters transmission curves
table_dir = data_dir / 'tables'  # Vizier tables

# Define urls for remote data
photometry_url = 'http://supernovae.in2p3.fr/sdss_snls_jla/jla_light_curves.tgz'
table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/A+A/568/A22'
