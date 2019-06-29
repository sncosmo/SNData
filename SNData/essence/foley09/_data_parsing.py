#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

import numpy as np
from astropy.io import ascii, fits
from astropy.table import Table

from . import _meta as meta
from ... import _utils as utils


@utils.require_data_path(meta.data_dir)
def get_available_tables():
    """Get numbers of available tables for this survey / data release"""

    return [1]


@utils.require_data_path(meta.data_dir)
def load_table(table_id):
    """Load a table from the data paper for this survey / data

    See ``get_available_tables`` for a list of valid table IDs.

    Args:
        table_id (int, str): The published table number or table name
    """

    if table_id not in get_available_tables():
        raise ValueError(f'Table {table_id} is not available.')

    readme_path = meta.table_dir / 'ReadMe'
    table_path = meta.table_dir / f'table{table_id}.dat'
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

    # Todo: Handle when some of the files didn't finish downloading
    return list(Table.read(meta.eso_summary_path)['Object'])


@utils.require_data_path(meta.data_dir)
def get_data_for_id(obj_id):
    """Returns data for a given object id

    See ``get_available_ids()`` for a list of available id values.

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of data for the given ID
    """

    summary_table = Table.read(meta.eso_summary_path)
    file_name = summary_table[summary_table['Object'] == obj_id]['ARCFILE'][0]
    hdul = fits.open(file_name)
    data_table = Table(
        np.array(hdul[1].data[0]).T,
        names=['WAVE', 'FLUX', 'ERR']
    )

    data_table.meta = dict(hdul[1].header)
    return data_table


def get_sncosmo_input(obj_id):
    """Returns an SNCosmo input table a given object ID

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of data formatted for use with SNCosmo
    """

    raise RuntimeError('Photometric data is not available for essence.foley09')


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
