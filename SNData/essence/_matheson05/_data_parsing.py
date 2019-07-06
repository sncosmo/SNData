#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from glob import glob

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

    readme_path = meta.vizier_dir / 'ReadMe'
    table_path = meta.vizier_dir / f'table{table_id}.dat'
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

    files = glob(str(meta.spectra_dir / '*.fits'))
    if not len(files) == 52:
        raise utils.NoDownloadedData()

    return sorted(set(Table.read(meta.eso_summary_path)['Object']))


# Todo: We are missing spectra
@utils.require_data_path(meta.data_dir)
def get_data_for_id(obj_id, format_sncosmo=False):
    """Returns data for a given object ID

    See ``get_available_ids()`` for a list of available ID values.

    Args:
        obj_id          (str): The ID of the desired object
        format_sncosmo (bool): Format data for SNCosmo.fit_lc (Default: False)

    Returns:
        An astropy table of data for the given ID
    """

    if format_sncosmo:
        raise RuntimeError(
            'Photometric data is not available for essence.matheson05')

    summary_table = Table.read(meta.eso_summary_path)
    file_name = summary_table[summary_table['Object'] == obj_id]['ARCFILE'][0]
    hdul = fits.open(meta.spectra_dir / (file_name + '.fits'))
    data_table = Table(
        np.array(hdul[1].data[0]).T,
        names=['WAVE', 'FLUX', 'ERR']
    )

    data_table.meta = dict(hdul[1].header)
    data_table.meta['obj_id'] = obj_id
    return data_table


iter_data = utils.factory_iter_data(get_available_ids, get_data_for_id)
