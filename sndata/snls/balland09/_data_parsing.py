#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from pathlib import Path

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
            names=['index', 'wavelength', 'flux', 'fluxerr'],
            format='ascii.basic',
            comment='[#]|[@]'
        )

        data_table.remove_columns('index')
        data_table['type'] = fpath.name.split('_')[0].lower()
        tables.append(data_table)

    out_table = vstack(tables)

    # Meta data from file
    # meta = out_table.meta['comments']
    del out_table.meta

    out_table.meta['obj_id'] = obj_id
    # out_table.meta['ra'] =
    # out_table.meta['dec'] =
    # out_table.meta['z'] = int(meta[2].split()[-1])
    # out_table.meta['z_err'] = None

    return out_table


iter_data = factory.factory_iter_data(get_available_ids, get_data_for_id)
