#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

from . import _meta as meta
from ... import _utils as utils

delete_module_data = utils.factory_delete_module_data(meta.data_dir)


def download_module_data(force=False):
    """Download data for the current survey / data release

    Args:
        force (bool): Re-Download locally available data (Default: False)
    """

    # Download data tables
    if force or not meta.table_dir.exists():
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

        # Mistakes in Table 3
        lines[186] = lines[186].replace('[53263.77/54960.03]?', '?=-')
        lines[189] = lines[189].replace('[0.06/2.71]?', '?')
        lines[190] = lines[190].replace('[53234.7/55165.94]?', '?=-')
        lines[193] = lines[193].replace('[0.6/1.24]?', '?')
        lines[194] = lines[194].replace('[0.278/1.993]?', '?=-')
        lines[195] = lines[195].replace('[0.01/0.175]?', '?')
        lines[196] = lines[196].replace('[0.734/2.256]?', '?=-')
        lines[198] = lines[198].replace('[0.036/0.198]?', '?')
        lines[199] = lines[199].replace('[0.301/1.188]?', '?=-')
        lines[201] = lines[201].replace('[0.005/1.761]?', '?')
        lines[202] = lines[202].replace('[0.06/1.28]?', '?=-')
        lines[204] = lines[204].replace('[0.06/0.067]?', '?')

        with open(meta.table_dir / 'ReadMe_formatted', 'w') as ofile:
            ofile.writelines(lines)

    # Download photometry
    if force or not meta.photometry_dir.exists():
        print('Downloading photometry...')
        utils.download_tar(
            url=meta.photometry_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    # Download filters
    if force or not meta.filter_dir.exists():
        print('Downloading filters...')
        for file_name in meta.filter_file_names:
            utils.download_file(
                url=meta.filter_url + file_name,
                out_file=meta.filter_dir / file_name)
