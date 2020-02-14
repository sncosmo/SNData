#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

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
    if (force or not meta.table_dir.exists()) \
            and utils.check_url(meta.table_url):
        print('Downloading data tables...')
        utils.download_tar(
            url=meta.table_url,
            out_dir=meta.table_dir,
            mode='r:gz')

    # Download spectra
    spec_urls = meta.phase_spectra_url, meta.snonly_spectra_url
    names = 'combined', 'supernova only'
    for spectra_url, data_name in zip(spec_urls, names):
        if (force or not meta.spectra_dir.exists()) \
                and utils.check_url(spectra_url):
            print(f'Downloading {data_name} spectra...')
            utils.download_tar(
                url=spectra_url,
                out_dir=meta.data_dir,
                mode='r:gz')
