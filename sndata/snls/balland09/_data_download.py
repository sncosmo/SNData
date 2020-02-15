#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

import os

from . import _meta as meta
from ... import _factory_funcs as factory
from ... import _utils as utils

delete_module_data = factory.factory_delete_module_data(meta.data_dir)


def download_module_data(force=False):
    """Download data for the current survey / data release

    Args:
        force (bool): Re-Download locally available data (Default: False)
    """

    # Download data tables
    if (force or not meta.table_dir.exists()) and utils.check_url(meta.table_url):
        print('Downloading data tables...')
        utils.download_tar(
            url=meta.table_url,
            out_dir=meta.table_dir,
            mode='r:gz')

    fix_balland09_cds_readme(meta.table_dir / 'ReadMe')

    # Download spectra
    if (force or not meta.spectra_dir.exists()):
        spec_urls = meta.phase_spectra_url, meta.snonly_spectra_url
        names = 'combined', 'supernova only'

        for spectra_url, data_name in zip(spec_urls, names):
            if utils.check_url(spectra_url):
                print(f'Downloading {data_name} spectra...')
                utils.download_tar(
                    url=spectra_url,
                    out_dir=meta.spectra_dir,
                    mode='r:gz')


def fix_balland09_cds_readme(readme_path):
    """Fix typos in the Balland 2009 CDS Readme so it is machine parsable

    Args:
        readme_path: Path of the README file to fix
    """

    # The downloaded files in this case are readonly, so we change permissions
    os.chmod(readme_path, 438)

    with open(readme_path, 'r+') as data_in:
        lines = data_in.readlines()
        lines[112] = lines[112].replace('? ', '?=- ')

        data_in.seek(0)
        data_in.writelines(lines)
