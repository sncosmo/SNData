#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from glob import glob
from os import path as _path

import numpy as np
from astropy.io import ascii

from . import _meta_data as meta_data
from ... import _utils as utils


def load_table(table_num):
    """Load a table from the data release paper"""

    readme_path = meta_data.tables_dir / 'ReadMe'
    table_path = meta_data.tables_dir / f'table{table_num}.dat'
    if not table_path.exists:
        raise ValueError(f'Table {table_num} is not available.')

    return ascii.read(table_path, format='cds', readme_path=readme_path)


def get_data_for_id(obj_id):
    """Returns photometric data for a supernova candidate in a given filter

    No data cuts are applied to the returned data.

    Args:
        obj_id (str): The Candidate ID of the desired object

    Returns:
        An astropy table of photometric data for the given candidate ID
    """

    file_path = _path.join(meta_data.photometry_dir, f'SN{obj_id}_snpy.txt')
    data_table = utils.parse_snoopy_data(file_path)
    data_table['band'] = 'SND_csp_' + data_table['band']
    data_table.meta['obj_id'] = obj_id

    return data_table


def _get_zp_for_bands(band):
    """Returns the zero point coresponding to any band in meta_data.band_names

    Args:
        band (list[str]): The name of a band

    Returns:
        An array of zero points
    """
    sorter = np.argsort(meta_data.band_names)
    indices = sorter[
        np.searchsorted(meta_data.band_names, band, sorter=sorter)]
    return np.array(meta_data.zero_point)[indices]


def get_input_for_id(obj_id):
    """Returns an SNCosmo input table a given CSP object ID

    No data cuts are applied to the returned data.

    Args:
        obj_id      (str): The ID of the desired object

    Returns:
        An astropy table of photometric data formatted for use with SNCosmo
    """

    sn_data = get_data_for_id(obj_id)
    sn_data['zp'] = _get_zp_for_bands(sn_data['band'])
    sn_data['zpsys'] = np.full(len(sn_data), 'ab')
    sn_data['flux'] = 10 ** ((sn_data['mag'] - sn_data['zp']) / -2.5)
    sn_data['fluxerr'] = \
        np.log(10) * sn_data['flux'] * sn_data['mag_err'] / 2.5

    sn_data.remove_columns(['mag', 'mag_err'])
    return sn_data


def get_obj_ids():
    """Return a list of target object ids for the current survey

    Returns:
        A list of object ids as strings
    """

    # Get target ids
    files = glob(_path.join(meta_data.photometry_dir, '*.txt'))
    return [_path.basename(f).split('_')[0].lstrip('SN') for f in files]


def iter_sncosmo_input(verbose=False):
    """Iterate through light-curves and yield the SNCosmo input tables

    Args:
        verbose (bool): Optionally display progress bar while iterating

    Yields:
        An astropy table formatted for use with SNCosmo
    """

    iter_data = utils.build_pbar(get_obj_ids(), verbose)
    for id_val in iter_data:
        sncosmo_table = get_input_for_id(id_val)
        if sncosmo_table:
            yield sncosmo_table
