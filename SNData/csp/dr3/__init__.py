#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to data from the third data release of the
Carnegie Supernova Project (CSP).
"""

from . import _meta_data
from ._data_parsing import get_data_for_id
from ._data_parsing import get_input_for_id
from ._data_parsing import iter_sncosmo_input
from ._meta_data import band_names
from ._meta_data import lambda_effective
from ._meta_data import lambda_effective
from ... import _utils

# Download data tables
if not _meta_data.tables_dir.exists():
    print('Downloading data tables...')
    _utils.download_tar(
        url='http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/AJ/154/211',
        out_dir=_meta_data.tables_dir,
        mode='r:gz')

# Download photometry
if not _meta_data.photometry_dir.exists():
    print('Downloading photometry...')
    _utils.download_tar(
        url='https://csp.obs.carnegiescience.edu/data/CSP_Photometry_DR3.tgz',
        out_dir=_meta_data.data_dir,
        mode='r:gz')

# Download photometry
if not _meta_data.filter_dir.exists():
    print('Downloading filters...')
    for file_name in _meta_data.filter_file_names:
        _utils.download_file(
            url='https://csp.obs.carnegiescience.edu/data/u_tel_ccd_atm_ext_1.2.dat',
            out_file=_meta_data.filter_dir / file_name)

# Register filters
for _file_name, _band_name in zip(_meta_data.filter_file_names, band_names):
    fpath = _meta_data.filter_dir / _file_name
    _utils.register_filter(fpath, _band_name)


def delete_module_data():
    """Delete any data downloaded by this module"""

    import shutil
    shutil.rmtree(_meta_data.data_dir)
