#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

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

    # Download photometry
    if not meta.photometry_dir.exists():
        print('Downloading photometry...')
        utils.download_tar(
            url=meta.photometry_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    # Download filters
    if not meta.filter_dir.exists():
        print('Downloading filters...')
        for file_name in meta.filter_file_names:
            utils.download_file(
                url=meta.filter_url,
                out_file=meta.filter_dir / file_name)


def delete_module_data():
    """Delete any data for the current survey / data release"""

    import shutil
    shutil.rmtree(meta.data_dir)
