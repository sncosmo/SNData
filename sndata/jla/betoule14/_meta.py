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
    4393.265,
    6242.36,
    6545.411,
    7705.673,
    4794.042,
    3628.672,
    7674.082,
    4358.25,
    5409.747,
    5491.773,
    'MEGACAMPSF::i',
    9052.537,
    7506.208,
    3562.166,
    11399.961,
    5387.569,
    3594.325,
    4355.833,
    'MEGACAMPSF::z', # Todo add megacam filters
    4717.598,
    3562.166,
    4405.525,
    'MEGACAMPSF::r',
    6186.798,
    5417.783,
    8019.814,
    6558.283,
    8044.647,
    8918.301,
    5957.935,
    6239.341,
    16101.54,
    3562.166,
    7630.763,
    'MEGACAMPSF::g'
]
