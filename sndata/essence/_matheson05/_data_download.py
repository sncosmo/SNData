#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

import requests
from astropy.table import Table

from . import _meta as meta
from ... import _utils as utils

delete_module_data = utils.factory_delete_module_data(meta.data_dir)


def download_module_data(force=False):
    """Download data for the current survey / data release

    Args:
        force (bool): Re-Download locally available data (Default: False)
    """

    # Download data tables
    if force or not meta.vizier_dir.exists():
        print('Downloading data tables...')
        utils.download_tar(
            url=meta.vizier_url,
            out_dir=meta.vizier_dir,
            mode='r:gz')

    if force or not meta.eso_summary_path.exists():
        print('Downloading spectra file list...')
        print(f'Fetching {meta.eso_summary_url}')
        r = requests.get(meta.eso_summary_url)

        # Strip header and footer and write to file
        table_content = '\n'.join(r.content.decode('utf8').split('\n')[1:-6])
        meta.eso_summary_path.parent.mkdir(exist_ok=True)
        with open(meta.eso_summary_path, 'w') as ofile:
            ofile.write(table_content)

    print('Downloading Spectra...')
    for row in Table.read(meta.eso_summary_path):
        file_path = meta.spectra_dir / (row['ARCFILE'] + '.fits')
        if force or not file_path.exists():
            url = meta.eso_spectra_url_pattern.format(row['ARCFILE'])
            utils.download_file(url, file_path)
