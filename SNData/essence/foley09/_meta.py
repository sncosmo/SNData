#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Download any data files that do not exist locally and define file paths to
the local data for use by the parent module.
"""

from pathlib import Path

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

# Define local paths of published data
spectra_dir = data_dir / 'spectra'
table_dir = data_dir / 'tables'

# Define urls for remote data
# photometry_url = 'https://csp.obs.carnegiescience.edu/data/CSP_Photometry_DR3.tgz'
table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/AJ/137/3731'
