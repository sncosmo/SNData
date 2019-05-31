#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from glob import glob
from os import path as _path

import numpy as np
from astropy.io import ascii

from . import _meta as meta
from ._data_download import _raise_for_data
from ... import _utils as utils


def register_filters():
    """Register filters for this survey / data release with SNCosmo"""

    _raise_for_data()
    for _file_name, _band_name in zip(meta.filter_file_names, meta.band_names):
        fpath = meta.filter_dir / _file_name
        utils.register_filter(fpath, _band_name)


def get_available_tables():
    """Get numbers of available tables for this survey / data release"""

    _raise_for_data()
    table_nums = []
    for f in meta.table_dir.rglob('table*.dat'):
        table_nums.append(int(f.stem.lstrip('table')))

    return table_nums


def load_table(table_num):
    """Load a table from the data paper for this survey / data

    Args:
        table_num (int): The published table number
    """

    _raise_for_data()

    readme_path = meta.table_dir / 'ReadMe'
    table_path = meta.table_dir / f'table{table_num}.dat'
    if not table_path.exists:
        raise ValueError(f'Table {table_num} is not available.')

    return ascii.read(str(table_path), format='cds', readme=str(readme_path))


def get_available_ids():
    """Return a list of target object ids for the current survey

    Returns:
        A list of object ids as strings
    """

    _raise_for_data()
    files = glob(_path.join(meta.photometry_dir, '*.txt'))
    return [_path.basename(f).split('_')[0].lstrip('SN') for f in files]


def _get_zp_for_bands(band):
    """Returns the zero point corresponding to any band in meta.band_names

    Args:
        band (list[str]): The name of a band

    Returns:
        An array of zero points
    """

    sorter = np.argsort(meta.band_names)
    indices = np.searchsorted(meta.band_names, band, sorter=sorter)

    return np.array(meta.zero_point)[sorter[indices]]


# noinspection PyPep8
def get_data_for_id(obj_id):
    """Returns data for a given object id

    No data cuts are applied to the returned data. See ``get_available_ids()``
    for a list of available id values.

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of data for the given ID
    """

    # Read data file for target
    _raise_for_data()
    file_path = _path.join(meta.photometry_dir, f'SN{obj_id}_snpy.txt')
    data_table = utils.parse_snoopy_data(file_path)

    # Add flux values
    data_table['band'] = 'csp_dr3_' + data_table['band']
    data_table['zp'] = _get_zp_for_bands(data_table['band'])
    data_table['zpsys'] = np.full(len(data_table), 'ab')
    data_table['flux'] = 10 ** ((data_table['mag'] - data_table['zp']) / -2.5)
    data_table['fluxerr'] = np.log(10) * data_table['flux'] * data_table['mag_err'] / 2.5

    return data_table


def iter_data(verbose=False):
    """Iterate through all available targets and yield data tables

    An optional progress bar can be formatted by passing a dictionary of tqdm
    arguments.

    Args:
        verbose (bool, dict): Optionally display progress bar while iterating

    Yields:
        Astropy tables
    """

    iterable = utils.build_pbar(get_available_ids(), verbose)
    for id_val in iterable:
        data_table = get_data_for_id(id_val)
        if data_table:
            yield data_table
