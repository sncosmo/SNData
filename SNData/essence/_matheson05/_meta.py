#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Download any data files that do not exist locally and define file paths to
the local data for use by the parent module.
"""

from pathlib import Path

# Define local paths of published data
_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'
spectra_dir = data_dir / 'spectra'
eso_summary_path = spectra_dir / 'target_summary.csv'
vizier_dir = data_dir / 'tables'

# Define URLs for remote data
vizier_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/AJ/137/3731'

# URL of table listing spectra file IDS
eso_summary_url = (
    'http://archive.eso.org/wdb/wdb/adp/phase3_main/query?'

    # Specify data we want
    '&wdbo=csv'
    '&prog_id=170.A-0519'
    '&tab_dp_id=on'
)

# Pattern for download link link for a given file ID
eso_spectra_url_pattern = 'http://archive.eso.org/datalink/links?ID=ivo://eso.org/ID?{}&eso_download=file'
