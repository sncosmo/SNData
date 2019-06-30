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

    if force or not meta.smp_dir.exists():
        print('Downloading SMP data...')
        utils.download_tar(
            url=meta.smp_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    if force or not meta.snana_dir.exists():
        print('Downloading SNANA data...')
        utils.download_tar(
            url=meta.snana_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    if force or not meta.master_table_path.exists():
        print('Downloading master table...')
        utils.download_file(
            url=meta.master_table_url,
            out_file=meta.master_table_path)

    if force or not meta.filter_dir.exists():
        print('Downloading filters...')
        for file_name in meta.filter_file_names:
            utils.download_file(
                url=meta.filter_url + file_name,
                out_file=meta.filter_dir / file_name)

        outlier_archive = meta.snana_dir / 'SDSS_allCandidates+BOSS.tar.gz'
        with tarfile.open(str(outlier_archive), mode='r:gz') as data:
            data.extractall(str(outlier_archive.parent))
