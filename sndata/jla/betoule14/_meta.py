#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module specifies file meta and urls used by this submodule."""

from pathlib import Path

import numpy as np

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

# Define local paths of published data
photometry_dir = data_dir / 'jla_light_curves'  # Photometry data
filter_dir = data_dir / 'filters'  # Filters transmission curves
table_dir = data_dir / 'tables'  # Vizier tables

# Define urls for remote data
photometry_url = 'http://supernovae.in2p3.fr/sdss_snls_jla/jla_light_curves.tgz'
table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/A+A/568/A22'

band_names = [
    '4SHOOTER2::B',
    '4SHOOTER2::I',
    '4SHOOTER2::R',
    '4SHOOTER2::Us',
    '4SHOOTER2::V',
    'ACSWF::F606W',
    'ACSWF::F775W',
    'ACSWF::F850LP',
    'KEPLERCAM::B',
    'KEPLERCAM::Us',
    'KEPLERCAM::V',
    'KEPLERCAM::i',
    'KEPLERCAM::r',
    'MEGACAMPSF::g',
    'MEGACAMPSF::i',
    'MEGACAMPSF::r',
    'MEGACAMPSF::z',
    'NICMOS2::F110W',
    'NICMOS2::F160W',
    'SDSS::g',
    'SDSS::i',
    'SDSS::r',
    'SDSS::u',
    'SDSS::z',
    'STANDARD::B',
    'STANDARD::I',
    'STANDARD::R',
    'STANDARD::U',
    'STANDARD::V',
    'SWOPE2::B',
    'SWOPE2::V',
    'SWOPE2::g',
    'SWOPE2::i',
    'SWOPE2::r',
    'SWOPE2::u'
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
