#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from pathlib import Path

from astropy.coordinates import Angle
from astropy.io import ascii
from astropy.table import Table, vstack

from . import _meta as meta
from ... import _factory_funcs as factory
from ... import _utils as utils
from ...exceptions import InvalidObjId


# noinspection PyUnusedLocal
def register_filters(force=False):
    """Register filters for this survey / data release with SNCosmo

    Args:
        force (bool): Whether to re-register a band if already registered
    """

    raise ValueError('SNLS Balland09 is a spectroscopic data release '
                     'and has no filters to register.')


@utils.require_data_path(meta.table_dir)
def get_available_tables():
    """Get table numbers for machine readable tables published in the paper
    for this data release"""

    table_nums = []
    for f in meta.table_dir.rglob('table*.dat'):
        table_number = f.stem.lstrip('table')
        table_nums.append(int(table_number))

    return sorted(table_nums)


@utils.lru_copy_cache(maxsize=None)
@utils.require_data_path(meta.table_dir)
def load_table(table_id):
    """Load a table from the data paper for this survey / data

    See ``get_available_tables`` for a list of valid table IDs.

    Args:
        table_id (int, str): The published table number or table name
    """

    readme_path = meta.table_dir / 'ReadMe'
    table_path = meta.table_dir / f'table{table_id}.dat'
    if not table_path.exists:
        raise ValueError(f'Table {table_id} is not available.')

    data = ascii.read(str(table_path), format='cds', readme=str(readme_path))
    description = utils.read_vizier_table_descriptions(readme_path)[table_id]
    data.meta['description'] = description
    return data


@utils.require_data_path(meta.spectra_dir)
def get_available_ids():
    """Return a list of target object IDs for the current survey

    Returns:
        A list of object IDs as strings
    """

    files = meta.spectra_dir.glob('*.dat')
    ids = (Path(f).name.split('_')[1] for f in files)
    return sorted(set(ids))


def _get_balland_meta(obj_id):
    """Get the ra, dec, redshift and redshift error for a Balland09 SN

    Args:
        obj_id (str): The Id of the Supernova
    """

    # Get Coordinates
    table1 = load_table(1)
    object_data = table1[table1['SN'] == obj_id][0]

    ra_hourangle = (object_data['RAh'], object_data['RAm'], object_data['RAs'])
    ra_deg = Angle(ra_hourangle, unit='hourangle').to('deg')

    sign = -1 if object_data['DE-'] == '-' else 1
    dec_deg = (
        sign * object_data['DEd'] +  # Already in degrees
        object_data['DEm'] / 60 +  # arcmin to degrees
        object_data['DEs'] / 60 / 60  # arcesc to degrees
    )

    # Get redshift
    table2 = load_table(2)
    object_data = table2[table2['SN'] == obj_id][0]
    z = object_data['z']
    z_err = object_data['e_z']

    return ra_deg.value, dec_deg, z, z_err


# noinspection PyUnusedLocal
@utils.require_data_path(meta.spectra_dir)
def get_data_for_id(obj_id, format_table=True):
    """Returns data for a given object ID

    See ``get_available_ids()`` for a list of available ID values.

    Args:
        obj_id        (str): The ID of the desired object
        format_table (bool): Format for use with ``sncosmo`` (Default: True)

    Returns:
        An astropy table of data for the given ID
    """

    if obj_id not in get_available_ids():
        raise InvalidObjId()

    tables = []
    for fpath in meta.spectra_dir.glob(f'*_{obj_id}_*_Balland_etal_09.dat'):
        data_table = Table.read(
            fpath,
            names=['pixel', 'wavelength', 'flux', 'fluxerr'],
            format='ascii.basic',
            comment='[#]|[@]'
        )

        data_table['type'] = fpath.name.split('_')[0].lower()
        data_table['phase'] = float(data_table.meta['comments'][7].split()[-1])
        tables.append(data_table)

    ra, dec, z, z_err = _get_balland_meta(obj_id)
    out_table = vstack(tables)

    out_table.meta['obj_id'] = obj_id
    out_table.meta['ra'] = ra
    out_table.meta['dec'] = dec
    out_table.meta['z'] = z
    out_table.meta['z_err'] = z_err

    out_table.meta.pop('comments')
    out_table.meta['comments'] = ''

    return out_table


iter_data = factory.factory_iter_data(get_available_ids, get_data_for_id)
