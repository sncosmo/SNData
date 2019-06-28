#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

import shutil

from . import _meta as meta
from ... import _utils as utils


def download_module_data():
    """Download data for the current survey / data release"""

    # Download data tables
    if not meta.table_dir.exists():
        print('Downloading data tables...')
        utils.download_tar(
            url=meta.table_url,
            out_dir=meta.table_dir,
            mode='r:gz')

    # Download spectra
    if not meta.spectra_dir.exists():
        print('Downloading spectra...')
        utils.download_tar(
            url=meta.spectra_url,
            out_dir=meta.data_dir,
            mode='r:gz')


def delete_module_data():
    """Delete any data for the current survey / data release"""

    try:
        shutil.rmtree(meta.data_dir)

    except FileNotFoundError:
        pass
