#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

import tarfile

from . import _meta as meta
from ... import _utils as utils

delete_module_data = utils.factory_delete_module_data(meta.data_dir)


def download_module_data(force=False):
    """Download data for the current survey / data release

    Args:
        force (bool): Re-Download locally available data (Default: False)
    """

    if (force or not meta.smp_dir.exists()) \
            and utils.check_url(meta.smp_url):

        print('Downloading SMP data...')
        utils.download_tar(
            url=meta.smp_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    if (force or not meta.snana_dir.exists()) \
            and utils.check_url(meta.snana_url):

        print('Downloading SNANA data...')
        utils.download_tar(
            url=meta.snana_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    if utils.check_url(meta.table_url):
        print(f'Downloading tables...')

        for file_name in meta.table_names:
            out_path = meta.table_dir / file_name
            if force or not out_path.exists():
                utils.download_file(
                    url=meta.table_url + file_name,
                    out_file=out_path
                )

    if utils.check_url(meta.filter_url):
        print(f'Downloading filters...')

        for file_name in meta.filter_file_names:
            out_path = meta.filter_dir / file_name
            if force or not out_path.exists():
                utils.download_file(
                    url=meta.filter_url + file_name,
                    out_file=out_path
                )
