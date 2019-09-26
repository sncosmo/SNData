#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from astropy.io import fits
from astropy.table import Column, Table

from . import _meta as meta
from ... import _utils as utils

# Cahce the master table for later use
_master_table = None


def register_filters(force=False):
    """Register filters for this survey / data release with SNCosmo

    Args:
        force (bool): Whether to re-register a band if already registered
    """

    raise ValueError('The ``sako18spec`` module is a spectroscopic data '
                     'release and has no filters to register. '
                     'See the ``sako18`` module for photometric data')


@utils.require_data_path(meta.data_dir)
def get_available_tables():
    """Get table numbers for machine readable tables published in the paper
    for this data release"""

    return ['master']


@utils.require_data_path(meta.data_dir)
def load_table(table_id):
    """Load a table from the data paper for this survey / data

    See ``get_available_tables`` for a list of valid table IDs.

    Args:
        table_id (int, str): The published table number or table name
    """

    if table_id == 'master':
        global _master_table
        if _master_table is None:
            _master_table = Table.read(meta.master_table_path, format='ascii')
            _master_table['CID'] = Column(_master_table['CID'], dtype=str)

        return _master_table

    else:
        raise ValueError(f'Table {table_id} is not available.')


@utils.require_data_path(meta.data_dir)
def get_available_ids():
    """Return a list of target object IDs for the current survey

    Returns:
        A list of object IDs as strings
    """

    return sorted(load_table('master')['CID'])


@utils.require_data_path(meta.data_dir)
def get_data_for_id(obj_id, format_table=True):
    """Returns data for a given object ID

    See ``get_available_ids()`` for a list of available ID values.

    Args:
        obj_id        (str): The ID of the desired object
        format_table (bool): Format data for ``SNCosmo`` (Default: True)

    Returns:
        An astropy table of data for the given ID
    """

    master_table = load_table('master')
    master_record = master_table[master_table['CID'] == obj_id][0]
    spectrum_id = master_record['SID']

    # Read in ascii data table for specified object
    file_path = meta.spectra_dir / f'gal{obj_id}-{spectrum_id}.fits'
    with fits.open(file_path, memmap=False) as hdulist:
        data = Table(rows=hdulist[0].data)
        data.meta.update(hdulist[0].header)

    data.meta['Type'] = master_record['Type']
    data.meta['zSN'] = master_record['zSN']
    data.meta['zGal'] = master_record['zGal']
    return data


iter_data = utils.factory_iter_data(get_available_ids, get_data_for_id)
