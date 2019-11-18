#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

import zipfile

from . import _meta as meta
from ... import _utils as utils

delete_module_data = utils.factory_delete_module_data(meta.data_dir)


def download_module_data(force=False):
    """Download data for the current survey / data release

    Args:
        force (bool): Re-Download locally available data (Default: False)
    """

    if (force or not meta.master_table_path.exists()) \
            and utils.check_url(meta.master_table_url):

        print('Downloading master table...')
        utils.download_file(
            url=meta.master_table_url,
            out_file=meta.master_table_path)

    # We download the master table of the photometric data release so
    # that we have access to the ra, dec, and z of each target
    if (force or not meta.photometry_master_table_path.exists()) \
            and utils.check_url(meta.master_table_url):

        print('Downloading target meta data...')
        utils.download_file(
            url=meta.photometry_master_table_url,
            out_file=meta.photometry_master_table_path)

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
