#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

import numpy as np
from astropy.table import Table

from . import _meta as meta
from ._data_download import _raise_for_data
from ... import _integrations as integrations
from ... import _utils as utils


def register_filters(force=False):
    """Register filters for this survey / data release with SNCosmo

    Args:
        force (bool): Whether to re-register a band if already registered
    """

    _raise_for_data()
    for _file_name, _band_name in zip(meta.filter_file_names, meta.band_names):
        fpath = meta.filter_dir / _file_name
        integrations.register_filter(fpath, _band_name, force=force)


def get_available_tables():
    """Get numbers of available tables for this survey / data release"""

    # _raise_for_data()
    raise RuntimeError('No Vizier tables available for this paper.')


# noinspection PyUnusedLocal
def load_table(table_num):
    """Load a table from the data paper for this survey / data

    Args:
        table_num (int): The published table number
    """

    # _raise_for_data()
    raise RuntimeError('No Vizier tables available for this paper.')


def get_available_ids():
    """Return a list of target object ids for the current survey

    Returns:
        A list of object ids as strings
    """

    _raise_for_data()

    # Load list of all target ids
    target_list_path = meta.photometry_dir / 'DES-SN3YR_DES.LIST'
    file_list = np.genfromtxt(target_list_path, dtype=str)
    return [f.lstrip('des_').rstrip('.dat') for f in file_list]


def get_data_for_id(obj_id):
    """Returns DES photometric data for a given object ID

    No data cuts are applied to the returned data.

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of photometric data for the given candidate ID
    """

    _raise_for_data()

    # Read in ascci data table for specified object
    file_path = meta.photometry_dir / f'des_{int(obj_id):08d}.dat'
    all_data = Table.read(
        file_path, format='ascii',
        data_start=27, data_end=-1,
        names=['VARLIST:', 'MJD', 'BAND', 'FIELD', 'FLUXCAL', 'FLUXCALERR',
               'ZPFLUX', 'PSF', 'SKYSIG', 'GAIN', 'PHOTFLAG', 'PHOTPROB'])

    # Add meta data to table
    with open(file_path) as ofile:
        table_meta_data = ofile.readlines()
        all_data.meta['ra'] = float(table_meta_data[7].split()[1])
        all_data.meta['dec'] = float(table_meta_data[8].split()[1])
        all_data.meta['PEAKMJD'] = float(table_meta_data[12].split()[1])
        all_data.meta['redshift'] = float(table_meta_data[13].split()[1])
        all_data.meta['redshift_err'] = float(table_meta_data[13].split()[3])
        all_data.meta['obj_id'] = obj_id
        del all_data.meta['comments']

    return all_data


def get_sncosmo_input(obj_id):
    """Returns an SNCosmo input table a given object ID

    Data points flagged in the SDSS II release as outliers are removed.

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of data formatted for use with SNCosmo
    """

    all_sn_data = get_data_for_id(obj_id)
    sncosmo_table = Table()
    sncosmo_table['time'] = all_sn_data['MJD']
    sncosmo_table['band'] = ['des_sn3yr_' + s for s in all_sn_data['BAND']]
    sncosmo_table['flux'] = all_sn_data['FLUXCAL']
    sncosmo_table['fluxerr'] = all_sn_data['FLUXCALERR']
    sncosmo_table['zp'] = np.full(len(all_sn_data), 27.5)
    sncosmo_table['zpsys'] = np.full(len(all_sn_data), 'ab')
    sncosmo_table.meta = all_sn_data.meta

    return sncosmo_table


def iter_data(verbose=False, format_sncosmo=False, filter_func=None):
    """Iterate through all available targets and yield data tables

    An optional progress bar can be formatted by passing a dictionary of tqdm
    arguments. Outputs can be optionally filtered by passing a function
    ``filter_func`` that accepts a data table and returns a boolean.

    Args:
        verbose  (bool, dict): Optionally display progress bar while iterating
        format_sncosmo (bool): Format data for SNCosmo.fit_lc (Default: False)
        filter_func    (func): An optional function to filter outputs by

    Yields:
        Astropy tables
    """

    if filter_func is None:
        filter_func = lambda x: x

    iterable = utils.build_pbar(get_available_ids(), verbose)
    for obj_id in iterable:
        if format_sncosmo:
            data_table = get_sncosmo_input(obj_id)

        else:
            data_table = get_data_for_id(obj_id)

        if filter_func(data_table):
            yield data_table
