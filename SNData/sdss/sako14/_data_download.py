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

    # Download photometry
    if not meta.smp_dir.exists():
        print('Downloading photometry...')
        utils.download_tar(
            url=meta.sdss_url,
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
