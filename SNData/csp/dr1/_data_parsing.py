#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from glob import glob
from pathlib import Path

import numpy as np
from astropy.io import ascii
from astropy.table import Column, Table, vstack

from . import _meta as meta
from ._data_download import _raise_for_data
from ... import _utils as utils


def get_available_tables():
    """Get numbers of available tables for this survey / data release"""

    table_nums = []
    for f in meta.table_dir.rglob('table*.dat'):
        table_nums.append(int(f.stem.lstrip('table')))

    return sorted(table_nums)


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

    files = glob(str(meta.spectra_dir / 'SN*.dat'))
    ids = ('20' + Path(f).name.split('_')[0].lstrip('SN') for f in files)
    return list(set(ids))


def _read_file(path):
    """Read a given file path of CSP DR1 data

    Args:
        path (str or Path): Path of file to read

    Returns:
        An astropy table with file data and meta data
    """

    # Handle single file with three columns
    path = Path(path)
    if path.stem == 'SN07bc_070409_b01_BAA_IM':
        data = Table.read(
            path, format='ascii', names=['wavelength', 'flux', '_'])
        data.remove_column('_')

    else:
        data = Table.read(path, format='ascii', names=['wavelength', 'flux'])

    # Get meta data for observation
    file_comments = data.meta['comments']
    redshift = float(file_comments[1].lstrip('Redshift: '))
    max_date = float(file_comments[2].lstrip('JDate_of_max: '))
    obs_date = float(file_comments[3].lstrip('JDate_of_observation: '))
    epoch = float(file_comments[4].lstrip('Epoch: '))

    _, _, wrange, telescope, instrument = path.stem.split('_')
    date_col = Column(data=np.full(len(data), obs_date), name='date')
    epoch_col = Column(data=np.full(len(data), epoch), name='epoch')
    wr_col = Column(data=np.full(len(data), wrange), name='wavelength_range')
    tel_col = Column(data=np.full(len(data), telescope), name='telescope')
    inst_col = Column(data=np.full(len(data), instrument), name='instrument')
    data.add_columns([date_col, epoch_col, wr_col, tel_col, inst_col])

    return max_date, redshift, data


def get_data_for_id(obj_id):
    """Returns data for a given object id

    See ``get_available_ids()`` for a list of available id values.

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of data for the given ID
    """

    _raise_for_data()

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

    # noinspection PyUnboundLocalVariable
    out_table.meta['redshift'] = redshift
    # noinspection PyUnboundLocalVariable
    out_table.meta['JDate_of_max'] = max_date
    out_table.meta['obj_id'] = obj_id

    return out_table


def get_sncosmo_input(obj_id):
    """Returns an SNCosmo input table a given object ID

    Data points flagged in the SDSS II release as outliers are removed.

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of data formatted for use with SNCosmo
    """

    raise RuntimeError('Photometric data is not available for csp.dr1')


# noinspection PyUnusedLocal
def iter_data(verbose=False, filter_func=None, **kwargs):
    """Iterate through all available targets and yield data tables

    An optional progress bar can be formatted by passing a dictionary of tqdm
    arguments. Outputs can be optionally filtered by passing a function
    ``filter_func`` that accepts a data table and returns a boolean.

    Args:
        verbose (bool, dict): Optionally display progress bar while iterating
        filter_func   (func): An optional function to filter outputs by

    Yields:
        Astropy tables
    """

    if filter_func is None:
        filter_func = lambda x: x

    iterable = utils.build_pbar(get_available_ids(), verbose)
    for id_val in iterable:
        data_table = get_data_for_id(id_val)
        if filter_func(data_table):
            yield data_table
