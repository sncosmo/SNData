#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

from . import _paths as paths
from ... import _utils as utils


def download_module_data():
    """Download data for the current survey / data release"""

    utils.download_data(
        base_url=_sdss_url,
        out_dir=data_dir,
        remote_name=_remote_data_file_names,
        check_local_name=_local_data_file_names
    )

    download_data(
        base_url=_filt_url,
        out_dir=filter_dir,
        remote_name=_local_filt_file_names,
        check_local_name=_local_filt_file_names
    )


def delete_module_data():
    """Delete any data for the current survey / data release"""

    import shutil
    shutil.rmtree(paths.data_dir)
