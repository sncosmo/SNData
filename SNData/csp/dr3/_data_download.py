#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

from . import _paths as paths
from ... import _utils as utils


def download_module_data():
    """Download data for the current survey / data release"""

    # Download data tables
    if not paths.table_dir.exists():
        print('Downloading data tables...')
        utils.download_tar(
            url=paths.table_url,
            out_dir=paths.table_dir,
            mode='r:gz')

    # Download photometry
    if not paths.photometry_dir.exists():
        print('Downloading photometry...')
        utils.download_tar(
            url=paths.photometry_url,
            out_dir=paths.data_dir,
            mode='r:gz')

    # Download filters
    if not paths.filter_dir.exists():
        print('Downloading filters...')
        for file_name in paths.filter_file_names:
            utils.download_file(
                url=paths.filter_url,
                out_file=paths.filter_dir / file_name)


def delete_module_data():
    """Delete any data for the current survey / data release"""

    import shutil
    shutil.rmtree(paths.data_dir)
