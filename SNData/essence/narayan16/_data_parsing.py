#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from glob import glob
from os import path as _path

import numpy as np
from astropy.io import ascii
from astropy.table import Table

from . import _meta as meta
from ... import _integrations as integrations
from ... import _utils as utils


@utils.require_data_path(meta.data_dir)
def register_filters(force=False):
    """Register filters for this survey / data release with SNCosmo

    Args:
        force (bool): Whether to re-register a band if already registered
    """

    for _file_name, _band_name in zip(meta.filter_file_names, meta.band_names):
        fpath = meta.filter_dir / _file_name
        integrations.register_filter(fpath, _band_name, force=force)


@utils.require_data_path(meta.data_dir)
def get_available_tables():
    """Get numbers of available tables for this survey / data release"""

    return [6]


@utils.require_data_path(meta.data_dir)
def load_table(table_id):
    """Load a table from the data paper for this survey / data

    See ``get_available_tables`` for a list of valid table IDs.

    Args:
        table_id (int, str): The published table number or table name
    """

    if table_id not in get_available_tables():
        raise ValueError(f'Table {table_id} is not available.')

    readme_path = meta.vizier_dir / 'ReadMe'
    table_path = meta.vizier_dir / f'table{table_id}.dat'
    data = ascii.read(str(table_path), format='cds', readme=str(readme_path))
    description = utils.read_vizier_table_descriptions(readme_path)[table_id]
    data.meta['description'] = description
    return data


@utils.require_data_path(meta.data_dir)
def get_available_ids():
    """Return a list of target object ids for the current survey

    Returns:
        A list of object ids as strings
    """

    files = glob(_path.join(meta.photometry_dir, '*.dat'))
    return sorted(_path.basename(f).split('.')[0] for f in files)


@utils.require_data_path(meta.data_dir)
def get_data_for_id(obj_id):
    """Returns data for a given object id

    See ``get_available_ids()`` for a list of available id values.

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of data for the given ID
    """

    path = meta.photometry_dir / f'{obj_id}.W6yr.clean.nn2.Wstd.dat'
    data_table = Table.read(
        path, format='ascii',
        names=['Observation', 'MJD', 'Passband', 'Flux', 'Fluxerr_lo',
               'Fluxerr_hi']
    )

    # Get meta data
    with open(path) as infile:
        keys = infile.readline().lstrip('# ').split()
        vals = infile.readline().lstrip('# ').split()

    for k, v in zip(keys, vals):
        data_table.meta[k] = v

    # Enforce uniformity across package
    data_table.meta['obj_id'] = data_table.meta.pop('objid')

    # Remove column names from table comments
    data_table.meta['comments'].pop()

    return data_table


def get_sncosmo_input(obj_id):
    """Returns an SNCosmo input table a given object ID

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of data formatted for use with SNCosmo
    """

    data_table = get_data_for_id(obj_id)
    out_table = Table()

    out_table['mjd'] = data_table['MJD']
    out_table['band'] = 'csp_dr3_' + data_table['Passband']
    out_table['zp'] = np.full(len(data_table), 25)
    out_table['zpsys'] = np.full(len(data_table), 'ab')
    out_table['flux'] = data_table['Flux']
    out_table['flux_err'] = np.max(
        [data_table['Fluxerr_hi'], data_table['Fluxerr_lo']], axis=0)

    return out_table


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
