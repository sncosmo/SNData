#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Download any data files that do not exist locally and define file paths to
the local data for use by the parent module.
"""

from pathlib import Path

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

# Define local paths of published data
vizier_dir = data_dir / 'vizier'
photometry_dir = vizier_dir / 'lcs'
filter_dir = data_dir / 'filters'

# Define urls for remote data
table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/ApJS/224/3'
r_filter_url = 'https://www.noao.edu/kpno/mosaic/filters/asc6004.f287.r04.txt'
i_filter_url = 'https://www.noao.edu/kpno/mosaic/filters/asc6028.f287.r04.txt'

filter_file_names = ('R_band.dat', 'I_band.dat')
band_names = ('essence_narayan16_R', 'essence_narayan16_I')
lambda_effective = (6440, 8050)
