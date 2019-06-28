#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

import os

import numpy as np
from astropy.table import Column, Table

from . import _meta as meta
from ... import _integrations as integrations
from ... import _utils as utils

# We will need to access the ``master table`` published by SDSS at various
# points so we lazy load it and keep it in memory
_master_table = None


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
    """Return a list of target object ids for the current survey

    Returns:
        A list of object ids as strings
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
    """Return the sncosmo band name given filter and CCD id

    Args:
        filter_id (int): Filter index 1 through 5 for 'ugriz'
        ccd_id    (int): Column number 1 through 6

    Args:
        The name of the filter registered with sncosmo
    """

    return f'sdss_sako18_{"ugriz"[filter_id]}{ccd_id}'


@utils.require_data_path(meta.data_dir)
def get_data_for_id(obj_id):
    """Returns data for a given object id

    See ``get_available_ids()`` for a list of available id values.

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of data for the given ID
    """

    # Read in ascii data table for specified object
    file_path = os.path.join(meta.smp_dir, f'SMP_{int(obj_id):06d}.dat')
    all_data = Table.read(file_path, format='ascii')

    # Rename columns using header data from file
    col_names = all_data.meta['comments'][-1].split()
    for i, name in enumerate(col_names):
        all_data[f'col{i + 1}'].name = name

    master_table = load_table('master')
    table_meta_data = master_table[master_table['CID'] == obj_id]
    all_data.meta['redshift'] = table_meta_data['zCMB'][0]
    all_data.meta['redshift_err'] = table_meta_data['zerrCMB'][0]
    all_data.meta['ra'] = table_meta_data['RA'][0]
    all_data.meta['dec'] = table_meta_data['DEC'][0]
    all_data.meta['classification'] = table_meta_data['Classification'][0]
    all_data.meta['name'] = table_meta_data['IAUName'][0]
    all_data.meta['obj_id'] = obj_id

    outlier_list = get_outliers().get(obj_id, [])
    if outlier_list:
        keep_indices = ~np.isin(all_data['MJD'], outlier_list)
        all_data = all_data[keep_indices]

    return all_data


def get_sncosmo_input(obj_id):
    """Returns an SNCosmo input table a given object ID

    Args:
        obj_id (str): The ID of the desired object

    Returns:
        An astropy table of data formatted for use with SNCosmo
    """

    # Format table
    phot_data = get_data_for_id(obj_id)
    if not phot_data:
        return Table(
            names=['time', 'band', 'zp', 'flux', 'fluxerr', 'zpsys', 'flag'])

    sncosmo_table = Table()
    sncosmo_table.meta = phot_data.meta
    sncosmo_table['time'] = phot_data['MJD']
    sncosmo_table['band'] = _construct_band_name(
        phot_data['FILT'], phot_data['IDCCD'])

    sncosmo_table['zp'] = np.full(len(phot_data), 2.5 * np.log10(3631))
    sncosmo_table['flux'] = phot_data['FLUX'] * 1E-6
    sncosmo_table['fluxerr'] = phot_data['FLUXERR'] * 1E-6
    sncosmo_table['zpsys'] = np.full(len(phot_data), 'ab')
    sncosmo_table['flag'] = phot_data['FLAG']

    return sncosmo_table


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
