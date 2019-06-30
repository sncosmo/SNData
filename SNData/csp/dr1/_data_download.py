#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

from . import _meta as meta
from ... import _utils as utils

delete_module_data = utils.factory_delete_module_data(meta.data_dir)


def download_module_data(force=False):
    """Download data for the current survey / data release

    Args:
        force (bool): Re-Download locally available data (Default: False)
    """

    # Download data tables
    if force or not meta.table_dir.exists():
        print('Downloading data tables...')
        utils.download_tar(
            url=meta.table_url,
            out_dir=meta.table_dir,
            mode='r:gz')

    # Download spectra
    if force or not meta.spectra_dir.exists():
        print('Downloading spectra...')
        utils.download_tar(
            url=meta.spectra_url,
            out_dir=meta.data_dir,
            mode='r:gz')
