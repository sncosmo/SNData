#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Download any data files that do not exist locally and define file paths to
the local data for use by the parent module.
"""

import os

from .._utils import download_data, register_filter

# Define local paths of published CSP data
_file_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(_file_dir, 'data')
photometry_dir = os.path.join(data_dir, 'DR3')  # DR3 Light Curves
filter_dir = os.path.join(data_dir, 'filters')  # DR3 Light Curves
krisciunas_dir = os.path.join(data_dir, 'Krisciunas_2013/')
master_path = os.path.join(data_dir, 'master.fits')

# Download Data from Krisciunas+ 13
krisciunas_tables = ['table1.dat', 'table2.dat', 'table3.dat']

vizier_url = 'http://cdsarc.u-strasbg.fr/ftp/J/AJ/154/211/'
download_data(
    base_url=vizier_url,
    out_dir=krisciunas_dir,
    remote_name=krisciunas_tables,
    check_local_name=krisciunas_tables)

# Download DR3 light curve data
_csp_url = 'https://csp.obs.carnegiescience.edu/data/'
download_data(
    base_url=_csp_url,
    out_dir=data_dir,
    remote_name=['CSP_Photometry_DR3.tgz'],
    check_local_name=[photometry_dir])

# Download DR3 filter profiles if they does not exist locally
_local_filt_names = [
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
]

# Register filters if not already registered
_band_names = ['u', 'g', 'r', 'i', 'B', 'V0', 'V1', 'V',
               'Y', 'H', 'J', 'Jrc2', 'Ydw', 'Jdw', 'Hdw']

band_names = [f'91bg_proj_csp_{f}' for f in _band_names]
lambda_effective = [3639.3, 4765.1, 6223.3, 7609.2, 4350.6, 5369.6, 5401.4,
                    5375.2, 10350.8, 12386.5, 12356.3, 16297.7, 10439.8,
                    12383.2, 16282.8]

zero_point = [12.986, 15.111, 14.902, 14.545, 14.328, 14.437, 14.393, 14.439,
              13.921, 13.836, 13.836, 13.510, 13.770, 13.866, 13.502]

download_data(
    base_url=_csp_url,
    out_dir=filter_dir,
    remote_name=_local_filt_names,
    check_local_name=_local_filt_names
)

for _filter_path, _filter_name in zip(_local_filt_names, band_names):
    fpath = os.path.join(filter_dir, _filter_path)
    filter_name = _filter_path.split('_')[0]
    register_filter(fpath, _filter_name)
