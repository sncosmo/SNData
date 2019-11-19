#!/usr/bin/env python3.7
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

    if (force or not meta.filter_dir.exists()) \
            and utils.check_url(meta.filter_url):

        print('Downloading filters...')
        utils.download_tar(
            url=meta.filter_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    if (force or not meta.photometry_dir.exists()) \
            and utils.check_url(meta.photometry_url):

        print('Downloading photometry...')
        utils.download_tar(
            url=meta.photometry_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    if (force or not meta.fits_dir.exists()) \
            and utils.check_url(meta.fits_url):

        print('Downloading Light-Curve Fits...')
        utils.download_tar(
            url=meta.fits_url,
            out_dir=meta.data_dir,
            mode='r:gz')
