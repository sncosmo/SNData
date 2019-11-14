#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from astropy.table import Column, Table, vstack

from . import _meta as meta
from ... import _utils as utils

# Cache the master table for later use
_master_table = None
_photometry_master_table = None


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
        format_table (bool): Format for use with ``sncosmo`` (Default: True)

    Returns:
        An astropy table of data for the given ID
    """

    master_table = load_table('master')

    data_tables = []
    for row in master_table[master_table['CID'] == obj_id]:
        for spec_type in row['Files'].split(','):
            file_name = f'{spec_type.lower()}{obj_id}-{row["SID"]}.txt'
            file_path = str(meta.spectra_dir / file_name)
            data = Table.read(file_path, format='ascii',
                              names=['wavelength', 'flux'])

            data['spec_type'] = spec_type
            data['date'] = row['Date']
            data['telescope'] = row['Telescope']
            data_tables.append(data)

    # Load target meta data from the master table of the photometric data
    global _photometry_master_table
    if _photometry_master_table is None:
        _photometry_master_table = Table.read(
            meta.photometry_master_table_path, format='ascii')

    phot_record_idx = _photometry_master_table['CID'] == int(obj_id)
    phot_record = _photometry_master_table[phot_record_idx][0]

    out_data = vstack(data_tables)
    out_data.meta['obj_id'] = obj_id
    out_data.meta['ra'] = phot_record['RA']
    out_data.meta['dec'] = phot_record['DEC']
    out_data.meta['z'] = phot_record['zCMB']
    out_data.meta['z_err'] = phot_record['zerrCMB']
    out_data.meta['dtype'] = 'spectroscopic'
    out_data.meta['comments'] = \
        'z represents CMB corrected redshift of the supernova.'

    return out_data


iter_data = utils.factory_iter_data(get_available_ids, get_data_for_id)
