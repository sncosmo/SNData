#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module specifies file meta and urls used by this submodule."""

from pathlib import Path

_file_dir = Path(__file__).resolve().parent
data_dir = _file_dir / 'data'

# Define local paths of published data
photometry_dir = data_dir / 'DR3'  # DR3 Light Curves
filter_dir = data_dir / 'filters'  # DR3 Filters
table_dir = data_dir / 'tables'  # DR3 paper tables

# Define urls for remote data
photometry_url = 'https://csp.obs.carnegiescience.edu/data/CSP_Photometry_DR3.tgz'
filter_url = 'https://csp.obs.carnegiescience.edu/data/'
table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/AJ/154/211'

# Filter information
filter_file_names = (
    'u_tel_ccd_atm_ext_1.2.dat',  # u
    'g_tel_ccd_atm_ext_1.2.dat',  # g
    'r_tel_ccd_atm_ext_1.2_new.dat',  # r
    'i_tel_ccd_atm_ext_1.2_new.dat',  # i
    'B_tel_ccd_atm_ext_1.2.dat',  # B
    'V_LC3014_tel_ccd_atm_ext_1.2.dat',  # V0
    'V_LC3009_tel_ccd_atm_ext_1.2.dat',  # V1
    'V_tel_ccd_atm_ext_1.2.dat',  # V
    'Y_SWO_TAM_scan_atm.dat',  # Y
    'J_old_retrocam_swope_atm.dat',  # J
    'J_SWO_TAM_atm.dat',  # Jrc2
    'H_SWO_TAM_scan_atm.dat',  # H
    'Y_texas_DUP_atm.dat',  # Ydw
    'J_texas_DUP_atm.dat',  # Jdw
    'H_texas_DUP_atm.dat'  # Hdw
)

_band_names = (
    'u', 'g', 'r', 'i', 'B', 'V0', 'V1',
    'V', 'Y', 'J', 'Jrc2', 'H', 'Ydw', 'Jdw', 'Hdw'
)

band_names = tuple(f'csp_dr3_{f}' for f in _band_names)
zero_point = (
    12.986, 15.111, 14.902, 14.545, 14.328, 14.437, 14.393,
    14.439, 13.921, 13.836, 13.836, 13.510, 13.770, 13.866, 13.502
)
lambda_effective = (
    3639.3, 4765.1, 6223.3, 7609.2, 4350.6, 5369.6, 5401.4,
    5375.2, 10350.8, 12386.5, 12356.3, 16297.7, 10439.8,
    12383.2, 16282.8)
