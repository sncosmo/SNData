#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides factory functions used to simplify the creation of
functionally similar methods used by different modules.
"""

import shutil

import numpy as np
import sncosmo

from . import _utils as utils
from ._utils import build_pbar


def _register_filter(file_path, filt_name, force=False):
    """Registers filter profiles with sncosmo if not already registered

    Assumes the file at ``file_path`` is a two column, white space delimited
    ascii table.

    Args:
        file_path (str): Path of an ascii table with wavelength (Angstrom)
                          and transmission columns
        filt_name (str): The name of the registered filter.
        force    (bool): Whether to re-register a band if already registered
    """

    # Get set of registered builtin and custom band passes
    available_bands = set(
        k[0] for k in sncosmo.bandpasses._BANDPASSES._loaders)

    available_bands.update(
        k[0] for k in sncosmo.bandpasses._BANDPASSES._instances)

    # Register the new bandpass
    if filt_name not in available_bands:
        filt_data = np.genfromtxt(file_path).T
        band = sncosmo.Bandpass(filt_data[0], filt_data[1])
        band.name = filt_name
        sncosmo.register(band, force=force)


def factory_register_filters(meta):
    @utils.require_data_path(meta.filter_dir)
    def register_filters(force=False):
        """Register filters for this survey / data release with SNCosmo

        Args:
            force (bool): Whether to re-register a band if already registered
        """

        for _file_name, _band_name in zip(meta.filter_file_names, meta.band_names):
            filter_path = meta.filter_dir / _file_name
            _register_filter(filter_path, _band_name, force=force)

    return register_filters


def factory_iter_data(id_func, data_func):
    def iter_data(verbose=False, format_table=True, filter_func=None):
        """Iterate through all available targets and yield data tables

        An optional progress bar can be formatted by passing a dictionary of
        ``tqdm`` arguments. Outputs can be optionally filtered by passing a
        function ``filter_func`` that accepts a data table and returns a
        boolean.

        Args:
            verbose  (bool, dict): Optionally display progress bar while iterating
            format_table   (bool): Format data for ``SNCosmo`` (Default: True)
            filter_func    (func): An optional function to filter outputs by

        Yields:
            Astropy tables
        """

        if filter_func is None:
            filter_func = lambda x: x

        iterable = build_pbar(id_func(), verbose)
        for obj_id in iterable:
            data_table = data_func(obj_id, format_table=format_table)
            if filter_func(data_table):
                yield data_table

    return iter_data


def factory_delete_module_data(*dirs):
    def delete_module_data():
        """Delete any data for the current survey / data release"""

        try:
            for data_dir in dirs:
                shutil.rmtree(data_dir)

        except FileNotFoundError:
            pass

    return delete_module_data
