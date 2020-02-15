#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This file specifies file meta and urls used by the parent module."""

import os
from pathlib import Path

from ... import _utils as utils

# General metadata
survey_name = 'Equation of State: Supernovae trace Cosmic Expansion'
survey_abbrev = 'ESSENCE'
release = 'narayan16'
survey_url = 'http://www.ctio.noao.edu/essence/'
data_type = 'photometric'
publications = ('Narayan et al. 2016',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2016ApJS..224....3N/abstract'

if 'SNDATA_DIR' in os.environ:
    data_dir = utils.create_data_dir(survey_name, release)

else:
    data_dir = Path(__file__).resolve().parent / 'data'


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
zero_point = tuple(27.5 for _ in band_names)
