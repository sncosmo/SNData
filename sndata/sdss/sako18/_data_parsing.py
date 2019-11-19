#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from functools import lru_cache

import numpy as np
from astropy.table import Column, Table

from . import _meta as meta
from ... import _factory_funcs as factory
from ... import _utils as utils
from ...exceptions import InvalidObjId


@utils.require_data_path(meta.table_dir)
def get_available_tables():
    """Get table numbers for machine readable tables published in the paper
    for this data release"""

    table_names = []
    for f in meta.table_dir.glob('*.txt'):
        table_num = f.stem.strip('Table_data')
        if table_num.isnumeric():
            table_num = int(table_num)

        table_names.append(table_num)

    return sorted(table_names, key=lambda x: 0 if x == 'master' else x)


@lru_cache(maxsize=None)
@utils.require_data_path(meta.table_dir)
def load_table(table_id):
    """Load a table from the data paper for this survey / data

    See ``get_available_tables`` for a list of valid table IDs.

    Args:
        table_id (int, str): The published table number or table name
    """

    if table_id not in get_available_tables():
        raise ValueError(f'Table {table_id} is not available.')

    if table_id == 'master':
        table = Table.read(meta.table_dir / 'master_data.txt', format='ascii')

    else:
        table = Table.read(
            meta.table_dir / f'Table{table_id}.txt', format='ascii')

    table['CID'] = Column(table['CID'], dtype=str)
    if table_id == 9:
        table['SID'] = Column(table['SID'], dtype=str)

    return table


@utils.require_data_path(meta.smp_dir)
def get_available_ids():
    """Return a list of target object IDs for the current survey

    Returns:
        A list of object IDs as strings
    """

    return sorted(load_table('master')['CID'])


def get_outliers():
    """Return a dictionary of data points marked by SDSS II as outliers

    Returns:
        A dictionary {<obj_id>: [<MJD of bad data point>, ...], ...}
    """

    out_dict = dict()
    with open(meta.outlier_path) as ofile:
        for line in ofile.readlines():
            if line.startswith('IGNORE:'):
                line_list = line.split()
                cid, mjd, band = line_list[1], line_list[2], line_list[3]
                if cid not in out_dict:
                    out_dict[str(cid)] = []

                out_dict[str(cid)].append(mjd)

    return out_dict


@np.vectorize
def _construct_band_name(filter_id, ccd_id):
    """Return the sncosmo band name given filter and CCD ID

    Args:
        filter_id (int): Filter index 1 through 5 for 'ugriz'
        ccd_id    (int): Column number 1 through 6

    Args:
        The name of the filter registered with sncosmo
    """

    return f'sdss_sako18_{"ugriz"[filter_id]}{ccd_id}'


def _format_sncosmo_table(data_table):
    """Format a data table for use with SNCosmo

    Args:
        data_table (Table): A data table returned by ``get_data_for_id``

    Returns:
        The same data in a new table following the SNCosmo data model
    """

    # Format table
    if not data_table:
        return Table(
            names=['time', 'band', 'zp', 'flux', 'fluxerr', 'zpsys', 'flag'])

    out_table = Table()
    out_table.meta = data_table.meta

    out_table['time'] = data_table['JD']
    out_table['band'] = _construct_band_name(
        data_table['FILT'], data_table['IDCCD'])

    out_table['zp'] = np.full(len(data_table), 2.5 * np.log10(3631))
    out_table['flux'] = data_table['FLUX'] * 1E-6
    out_table['fluxerr'] = data_table['FLUXERR'] * 1E-6
    out_table['zpsys'] = np.full(len(data_table), 'ab')
    out_table['flag'] = data_table['FLAG']

    return out_table


@utils.require_data_path(meta.smp_dir)
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

    # Read in ascii data table for specified object
    file_path = meta.smp_dir / f'SMP_{int(obj_id):06d}.dat'
    data = Table.read(file_path, format='ascii')

    # Rename columns using header data from file
    col_names = data.meta['comments'][-1].split()
    for i, name in enumerate(col_names):
        data[f'col{i + 1}'].name = name

    data['JD'] = utils.convert_to_jd(data['MJD'])

    # Add meta data
    master_table = load_table('master')
    table_meta_data = master_table[master_table['CID'] == obj_id]
    data.meta['obj_id'] = obj_id
    data.meta['ra'] = table_meta_data['RA'][0]
    data.meta['dec'] = table_meta_data['DEC'][0]
    data.meta['z'] = table_meta_data['zCMB'][0]
    data.meta['z_err'] = table_meta_data['zerrCMB'][0]
    data.meta['dtype'] = 'photometric'
    data.meta['comments'] = \
        'z represents CMB corrected redshift of the supernova.'
    data.meta['classification'] = table_meta_data['Classification'][0]

    outlier_list = get_outliers().get(obj_id, [])
    if outlier_list:
        keep_indices = ~np.isin(data['MJD'], outlier_list)
        data = data[keep_indices]

    if format_table:
        data = _format_sncosmo_table(data)

    return data


register_filters = factory.factory_register_filters(meta)
iter_data = factory.factory_iter_data(get_available_ids, get_data_for_id)
