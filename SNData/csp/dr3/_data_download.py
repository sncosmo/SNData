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
        raise utils.NoDownloadedData(
            'Data has not been downloaded for this survey. '
            'Please run the ``download_data`` function.')


def download_module_data():
    """Download data for the current survey / data release"""

    # Download data tables
    if not meta.table_dir.exists():
        print('Downloading data tables...')
        utils.download_tar(
            url=meta.table_url,
            out_dir=meta.table_dir,
            mode='r:gz')

    # Fix formatting of CDS Readme
    with open(meta.table_dir / 'ReadMe') as ofile:
        lines = ofile.readlines()

    # Mistakes in Table 2
    lines[148] = lines[148].replace('[0.734/2.256]?', '?=-')
    lines[150] = lines[150].replace('[0.036/0.198]?', '?')
    lines[153] = lines[153].replace('Wang et al.', '?=- Wang et al.')
    lines[155] = lines[155].replace('Branch et al.', '?=- Branch et al.')
    lines[161] = lines[161].replace('[-11/66]?', '?=-')

    with open(meta.table_dir / 'ReadMe_formatted', 'w') as ofile:
        ofile.writelines(lines)

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
                url=meta.filter_url + file_name,
                out_file=meta.filter_dir / file_name)


def delete_module_data():
    """Delete any data for the current survey / data release"""

    import shutil

    try:
        shutil.rmtree(meta.data_dir)

    except FileNotFoundError:
        pass
