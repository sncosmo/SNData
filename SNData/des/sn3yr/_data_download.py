#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

from . import _meta as meta
from ... import _utils as utils


def data_is_available():
    """Return whether data has been downloaded for this survey / data release

    Returns
        A boolean
    """

    return meta.data_dir.exists()


def _raise_for_data():
    """Raise a RuntimeError if data hasn't been downloaded for this module"""

    if not data_is_available():
        raise RuntimeError(
            'Data has not been downloaded for this survey. '
            'Please run the ``download_data`` function.')


def download_module_data():
    """Download data for the current survey / data release"""

    # Download filter profiles
    if not meta.filter_dir.exists():
        print('Downloading filters...')
        utils.download_tar(
            url=meta.filter_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    # Download photometry
    if not meta.photometry_dir.exists():
        print('Downloading photometry...')
        utils.download_tar(
            url=meta.photometry_url,
            out_dir=meta.data_dir,
            mode='r:gz')


def delete_module_data():
    """Delete any data for the current survey / data release"""

    import shutil

    try:
        shutil.rmtree(meta.data_dir)

    except FileNotFoundError:
        pass
