#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from glob import glob
from pathlib import Path

import numpy as np
from astropy.io import ascii
from astropy.table import Column, Table, vstack

from . import _meta as meta
from ... import _utils as utils


def register_filters(force=False):
    """Register filters for this survey / data release with SNCosmo

    Args:
        force (bool): Whether to re-register a band if already registered
    """

    raise ValueError('CSP DR1 is a spectroscopic data release '
                     'and has no filters to register.')


@utils.require_data_path(meta.data_dir)
def get_available_tables():
    """Get table numbers for machine readable tables published in the paper
    for this data release"""

    table_nums = []
    for f in meta.table_dir.rglob('table*.dat'):
        table_number = f.stem.lstrip('table')
        table_nums.append(int(table_number))

    return sorted(table_nums)


@utils.require_data_path(meta.data_dir)
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


@utils.require_data_path(meta.data_dir)
def get_available_ids():
    """Return a list of target object IDs for the current survey

    Returns:
        A list of object IDs as strings
    """

    files = glob(str(meta.spectra_dir / 'SN*.dat'))
    ids = ('20' + Path(f).name.split('_')[0].lstrip('SN') for f in files)
    return sorted(set(ids))


def _read_file(path):
    """Read a file path of spectroscopic data from CSP DR1

    Args:
        path (str or Path): Path of file to read

    Returns:
        The data of maximum for the observed target
        The redshift of the target
        An astropy table with file data and meta data
    """

    # Handle the single file with a different data model:
    # There are three columns instead of two
    path = Path(path)
    if path.stem == 'SN07bc_070409_b01_BAA_IM':
        data = Table.read(path, format='ascii', names=['wavelength', 'flux', '_'])
        data.remove_column('_')

    else:
        data = Table.read(path, format='ascii', names=['wavelength', 'flux'])

    # Get various data from the table meta data
    file_comments = data.meta['comments']
    redshift = float(file_comments[1].lstrip('Redshift: '))
    max_date = float(file_comments[2].lstrip('JDate_of_max: '))
    obs_date = float(file_comments[3].lstrip('JDate_of_observation: '))
    epoch = float(file_comments[4].lstrip('Epoch: '))

    # Add remaining columns. These values are constant for a single file
    # (i.e. a single spectrum) but vary across files (across spectra)
    _, _, wrange, telescope, instrument = path.stem.split('_')
    date_col = Column(data=np.full(len(data), obs_date), name='date')
    epoch_col = Column(data=np.full(len(data), epoch), name='epoch')
    wr_col = Column(data=np.full(len(data), wrange), name='wavelength_range')
    tel_col = Column(data=np.full(len(data), telescope), name='telescope')
    inst_col = Column(data=np.full(len(data), instrument), name='instrument')
    data.add_columns([date_col, epoch_col, wr_col, tel_col, inst_col])

    # Ensure dates are in JD format
    data['date'] = utils.convert_to_jd(data['date'])

    return max_date, redshift, data


# noinspection PyUnboundLocalVariable
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

    out_table = Table(
        names=['date', 'wavelength', 'flux', 'epoch', 'wavelength_range',
               'telescope', 'instrument'],
        dtype=[float, float, float, float, 'U3', 'U3', 'U2']
    )

    files = meta.spectra_dir.rglob(f'SN{obj_id[2:]}_*.dat')
    if not files:
        raise ValueError(f'No data found for obj_id {obj_id}')

    for path in files:
        max_date, redshift, spectral_data = _read_file(path)
        out_table = vstack([out_table, spectral_data])

    out_table.meta['redshift'] = redshift
    out_table.meta['JDate_of_max'] = max_date
    out_table.meta['obj_id'] = obj_id

    return out_table


iter_data = utils.factory_iter_data(get_available_ids, get_data_for_id)
