#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

import tarfile
import zipfile

from . import _meta as meta
from ... import _factory_funcs as factory
from ..._utils import check_url, download_file, download_tar

delete_module_data = factory.factory_delete_module_data(meta.data_dir)


def download_module_data(force=False):
    """Download data for the current survey / data release

    Args:
        force (bool): Re-Download locally available data (Default: False)
    """

    # Photometry
    if (force or not meta.smp_dir.exists()) and check_url(meta.smp_url):
        print('Downloading SMP data...')
        download_tar(
            url=meta.smp_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    # SNANA files - including files specifying "bad" photometry data points
    if (force or not meta.snana_dir.exists()) and check_url(meta.snana_url):
        print('Downloading SNANA data...')
        download_tar(
            url=meta.snana_url,
            out_dir=meta.data_dir,
            mode='r:gz')

        # Unzip file listing "bad" photometry
        outlier_archive = meta.snana_dir / 'SDSS_allCandidates+BOSS.tar.gz'
        with tarfile.open(str(outlier_archive), mode='r:gz') as data:
            data.extractall(str(outlier_archive.parent))

    # Tables from the published paper
    print_tables = True  # Whether to print the status
    if check_url(meta.base_url):
        for file_name in meta.table_names:

            out_path = meta.table_dir / file_name
            if force or not out_path.exists():
                if print_tables:
                    print(f'Downloading tables...')
                    print_tables = False

                download_file(
                    url=meta.base_url + file_name,
                    out_file=out_path
                )

    # Photometric filters
    print_photometric = True
    if check_url(meta.filter_url):
        for file_name in meta.filter_file_names:

            out_path = meta.filter_dir / file_name
            if force or not out_path.exists():
                if print_photometric:
                    print(f'Downloading filters...')
                    print_photometric = False

                download_file(
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
