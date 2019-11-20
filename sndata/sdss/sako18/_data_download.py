#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

import tarfile
import zipfile

from . import _meta as meta
from ... import _factory_funcs as factory
from ... import _utils as utils

delete_module_data = factory.factory_delete_module_data(meta.data_dir)


def download_module_data(force=False):
    """Download data for the current survey / data release

    Args:
        force (bool): Re-Download locally available data (Default: False)
    """

    # Photometry
    if (force or not meta.smp_dir.exists()) \
            and utils.check_url(meta.smp_url):

        print('Downloading SMP data...')
        utils.download_tar(
            url=meta.smp_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    # SNANA files - including files specifying "bad" photometry data points
    if (force or not meta.snana_dir.exists()) \
            and utils.check_url(meta.snana_url):

        print('Downloading SNANA data...')
        utils.download_tar(
            url=meta.snana_url,
            out_dir=meta.data_dir,
            mode='r:gz')

        outlier_archive = meta.snana_dir / 'SDSS_allCandidates+BOSS.tar.gz'
        with tarfile.open(str(outlier_archive), mode='r:gz') as data:
            data.extractall(str(outlier_archive.parent))

    # Paper tables
    if utils.check_url(meta.table_url):
        for i, file_name in enumerate(meta.table_names):
            out_path = meta.table_dir / file_name
            if force or not out_path.exists():
                if i == 0:
                    print(f'Downloading tables...')

                utils.download_file(
                    url=meta.table_url + file_name,
                    out_file=out_path
                )

    # Photometric filters
    if utils.check_url(meta.filter_url):
        for i, file_name in enumerate(meta.filter_file_names):
            out_path = meta.filter_dir / file_name
            if force or not out_path.exists():
                if i == 0:
                    print(f'Downloading filters...')

                utils.download_file(
                    url=meta.filter_url + file_name,
                    out_file=out_path
                )

    # if (force or not meta.spectra_dir.exists()) \
    #         and utils.check_url(meta.spectra_url):
    #     print('Downloading spectra...')
    #     utils.download_tar(
    #         url=meta.spectra_url,
    #         out_dir=meta.data_dir,
    #         mode='r:gz')

    # Spectral data parsing requires IRAF so we use preparsed data instead
    if force or not meta.spectra_dir.exists():
        print('Unzipping spectra...')
        with zipfile.ZipFile(meta.spectra_zip, 'r') as zip_ref:
            zip_ref.extractall(meta.data_dir)
