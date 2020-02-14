#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This file specifies file meta and urls used by the parent module."""

import os
from pathlib import Path

import numpy as np

from ... import _utils as utils

# General metadata
survey_name = 'Joint Light-curve Analysis'
survey_abbrev = 'JLA'
release = 'betoule14'
survey_url = 'http://supernovae.in2p3.fr/sdss_snls_jla/ReadMe.html'
data_type = 'photometric'
publications = ('Betoule et al. (2014)',)
ads_url = 'https://ui.adsabs.harvard.edu/abs/2014A%26A...568A..22B/abstract'

if 'SNDATA_DIR' in os.environ:
    data_dir = utils.create_data_dir(survey_name, release)

else:
    data_dir = Path(__file__).resolve().parent / 'data'


# Define local paths of published data
photometry_dir = data_dir / 'jla_light_curves'  # Photometry data
table_dir = data_dir / 'tables'  # Vizier tables
filter_path = data_dir / 'cfht_filters.txt'

# Define urls for remote data
photometry_url = 'http://supernovae.in2p3.fr/sdss_snls_jla/jla_light_curves.tgz'
table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/A+A/568/A22'
filter_url = 'http://www.cfht.hawaii.edu/Instruments/Imaging/Megacam/data.MegaPrime/MegaCam_Filters_data_SAGEM.txt'

band_names = [
    'jla_betoule14_4SHOOTER2::B',
    'jla_betoule14_4SHOOTER2::I',
    'jla_betoule14_4SHOOTER2::R',
    'jla_betoule14_4SHOOTER2::Us',
    'jla_betoule14_4SHOOTER2::V',
    'jla_betoule14_ACSWF::F606W',
    'jla_betoule14_ACSWF::F775W',
    'jla_betoule14_ACSWF::F850LP',
    'jla_betoule14_KEPLERCAM::B',
    'jla_betoule14_KEPLERCAM::Us',
    'jla_betoule14_KEPLERCAM::V',
    'jla_betoule14_KEPLERCAM::i',
    'jla_betoule14_KEPLERCAM::r',
    'jla_betoule14_MEGACAMPSF::g',
    'jla_betoule14_MEGACAMPSF::i',
    'jla_betoule14_MEGACAMPSF::r',
    'jla_betoule14_MEGACAMPSF::z',
    'jla_betoule14_NICMOS2::F110W',
    'jla_betoule14_NICMOS2::F160W',
    'jla_betoule14_SDSS::g',
    'jla_betoule14_SDSS::i',
    'jla_betoule14_SDSS::r',
    'jla_betoule14_SDSS::u',
    'jla_betoule14_SDSS::z',
    'jla_betoule14_STANDARD::B',
    'jla_betoule14_STANDARD::I',
    'jla_betoule14_STANDARD::R',
    'jla_betoule14_STANDARD::U',
    'jla_betoule14_STANDARD::V',
    'jla_betoule14_SWOPE2::B',
    'jla_betoule14_SWOPE2::V',
    'jla_betoule14_SWOPE2::g',
    'jla_betoule14_SWOPE2::i',
    'jla_betoule14_SWOPE2::r',
    'jla_betoule14_SWOPE2::u'
]

lambda_effective = [
    4358.25,
    8019.814,
    6558.283,
    3562.166,
    5417.783,
    5957.935,
    7705.673,
    9052.537,
    4355.833,
    3562.166,
    5409.747,
    7674.082,
    6242.36,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    11399.961,
    16101.54,
    4717.598,
    7506.208,
    6186.798,
    3594.325,
    8918.301,
    4393.265,
    8044.647,
    6545.411,
    3562.166,
    5491.773,
    4405.525,
    5387.569,
    4794.042,
    7630.763,
    6239.341,
    3628.672
]

zero_point = [
    15.34721,
    14.465326,
    15.067505,
    14.205682,
    14.97444,
    17.21704,
    16.178942,
    15.833444,
    15.358495,
    14.205682,
    14.951837,
    14.962131,
    15.235409,
    27.045017,
    26.340862,
    26.494886,
    25.310699,
    16.733045,
    15.494573,
    27.5,
    27.5,
    27.5,
    27.5,
    27.5,
    15.277109,
    14.589873,
    15.05484,
    14.205682,
    14.841261,
    14.319437,
    14.522684,
    15.127543,
    14.777211,
    14.909701,
    13.036368
]
