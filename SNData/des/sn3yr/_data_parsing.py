#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

import numpy as np
from astropy.table import Table

from . import _meta as meta
from ... import _integrations as integrations
from ... import _utils as utils


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

    return ['SALT2mu_DES+LOWZ_C11.FITRES', 'SALT2mu_DES+LOWZ_G10.FITRES']


@utils.require_data_path(meta.data_dir)
def load_table(table_id):
    """Load a table from the data paper for this survey / data

    See ``get_available_tables`` for a list of valid table IDs.

    Args:
        table_id (int, str): The published table number or table name
    """

    if table_id not in get_available_tables():
        raise ValueError(f'Table {table_id} is not available.')

    data = Table.read(
        str(meta.fits_dir / table_id),
        format='ascii',
        data_start=4,
        comment='#',
        exclude_names=['dummy_col'],
        names=['dummy_col', 'CID', 'CIDint', 'IDSURVEY', 'TYPE', 'FIELD',
               'CUTFLAG_SNANA', 'zHEL', 'zHELERR', 'zCMB', 'zCMBERR',
               'zHD', 'zHDERR', 'VPEC', 'VPECERR', 'HOST_LOGMASS',
               'HOST_LOGMASS_ERR', 'SNRMAX1', 'SNRMAX2', 'SNRMAX3', 'PKMJD',
               'PKMJDERR', 'x1', 'x1ERR', 'c', 'cERR', 'mB', 'mBERR', 'x0',
               'x0ERR', 'COV_x1_c', 'COV_x1_x0', 'COV_c_x0', 'NDOF',
               'FITCHI2', 'FITPROB', 'RA', 'DECL', 'TGAPMAX', 'TrestMIN',
               'TrestMAX', 'MWEBV', 'm0obs_i', 'm0obs_r', 'em0obs_i',
               'em0obs_r',
               'MU', 'MUMODEL', 'MUERR', 'MUERR_RAW', 'MURES', 'MUPULL',
               'M0DIF',
               'ERRCODE', 'biasCor_mu', 'biasCorErr_mu', 'biasCor_mB',
               'biasCor_x1', 'biasCor_c', 'biasScale_muCOV', 'IDSAMPLE'])

    return data


@utils.require_data_path(meta.data_dir)
def get_available_ids():
    """Return a list of target object IDs for the current survey

    Returns:
        A list of object IDs as strings
    """

    # Load list of all target IDs
    target_list_path = meta.photometry_dir / 'DES-SN3YR_DES.LIST'
    file_list = np.genfromtxt(target_list_path, dtype=str)
    return sorted(f.lstrip('des_').rstrip('.dat') for f in file_list)


def _format_sncosmo_table(data_table):
    """Format a data table for use with SNCosmo

    Args:
        data_table (Table): A data table returned by ``get_data_for_id``

    Returns:
        The same data in a new table following the SNCosmo data model
    """

    out_table = Table()
    out_table.meta = data_table.meta

    out_table['time'] = data_table['MJD']
    out_table['band'] = ['des_sn3yr_' + s for s in data_table['BAND']]
    out_table['flux'] = data_table['FLUXCAL']
    out_table['fluxerr'] = data_table['FLUXCALERR']
    out_table['zp'] = np.full(len(data_table), 27.5)
    out_table['zpsys'] = np.full(len(data_table), 'ab')
    return out_table


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

    # Read in ascci data table for specified object
    file_path = meta.photometry_dir / f'des_{int(obj_id):08d}.dat'
    data = Table.read(
        file_path, format='ascii',
        data_start=27, data_end=-1,
        names=['VARLIST:', 'MJD', 'BAND', 'FIELD', 'FLUXCAL', 'FLUXCALERR',
               'ZPFLUX', 'PSF', 'SKYSIG', 'GAIN', 'PHOTFLAG', 'PHOTPROB'])

    # Add meta data to table
    with open(file_path) as ofile:
        table_meta_data = ofile.readlines()
        data.meta['ra'] = float(table_meta_data[7].split()[1])
        data.meta['dec'] = float(table_meta_data[8].split()[1])
        data.meta['PEAKMJD'] = float(table_meta_data[12].split()[1])
        data.meta['redshift'] = float(table_meta_data[13].split()[1])
        data.meta['redshift_err'] = float(table_meta_data[13].split()[3])
        data.meta['obj_id'] = obj_id
        del data.meta['comments']

    if format_sncosmo:
        data = _format_sncosmo_table(data)

    return data


iter_data = utils.factory_iter_data(get_available_ids, get_data_for_id)
