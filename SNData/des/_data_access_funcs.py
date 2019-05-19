#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from os import path as _path

import numpy as np
from astropy.table import Table

from . import _module_meta_data as meta_data
from .. import _utils as utils

master_table = Table.read(
    meta_data.master_table_path,
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
           'TrestMAX', 'MWEBV', 'm0obs_i', 'm0obs_r', 'em0obs_i', 'em0obs_r',
           'MU', 'MUMODEL', 'MUERR', 'MUERR_RAW', 'MURES', 'MUPULL', 'M0DIF',
           'ERRCODE', 'biasCor_mu', 'biasCorErr_mu', 'biasCor_mB',
           'biasCor_x1', 'biasCor_c', 'biasScale_muCOV', 'IDSAMPLE'])


def get_data_for_id(cid):
    """Returns DES photometric data for a given object ID

    No data cuts are applied to the returned data.

    Args:
        cid (str): The ID of the desired object

    Returns:
        An astropy table of photometric data for the given candidate ID
    """

    # Read in ascci data table for specified object
    file_path = _path.join(meta_data.photometry_dir, f'des_{int(cid):08d}.dat')
    all_data = Table.read(
        file_path, format='ascii',
        data_start=27, data_end=-1,
        names=['VARLIST:', 'MJD', 'BAND', 'FIELD', 'FLUXCAL', 'FLUXCALERR',
               'ZPFLUX', 'PSF', 'SKYSIG', 'GAIN', 'PHOTFLAG', 'PHOTPROB'])

    # Add meta data to table
    with open(file_path) as ofile:
        table_meta_data = ofile.readlines()
        all_data.meta['ra'] = float(table_meta_data[7].split()[1])
        all_data.meta['dec'] = float(table_meta_data[8].split()[1])
        all_data.meta['PEAKMJD'] = float(table_meta_data[12].split()[1])
        all_data.meta['redshift'] = float(table_meta_data[13].split()[1])
        all_data.meta['redshift_err'] = float(table_meta_data[13].split()[3])
        all_data.meta['cid'] = cid
        del all_data.meta['comments']

    return all_data


def get_input_for_id(cid, bands=None):
    """Returns an SNCosmo input table a given DES object ID

    No data cuts are applied to the returned data.

    Args:
        cid         (int): The ID of the desired object
        bands (list[str]): Optionally only return select bands (eg. 'desg')

    Returns:
        An astropy table of photometric data formatted for use with SNCosmo
    """

    all_sn_data = get_data_for_id(cid)
    sncosmo_table = Table()
    sncosmo_table['time'] = all_sn_data['MJD']
    sncosmo_table['band'] = ['des' + s for s in all_sn_data['BAND']]
    sncosmo_table['flux'] = all_sn_data['FLUXCAL']
    sncosmo_table['fluxerr'] = all_sn_data['FLUXCALERR']
    sncosmo_table['zp'] = np.full(len(all_sn_data), 27.5)
    sncosmo_table['zpsys'] = np.full(len(all_sn_data), 'ab')
    sncosmo_table.meta = all_sn_data.meta

    return sncosmo_table


def get_target_ids():
    """Return a list of target CID values

    Returns:
        A list of CID values
    """

    # Load list of all target ids
    target_list_path = _path.join(meta_data.photometry_dir,
                                  'DES-SN3YR_DES.LIST')
    file_list = np.genfromtxt(target_list_path, dtype=str)
    return [f.lstrip('des_').rstrip('.dat') for f in file_list]


def iter_sncosmo_input(bands=None, verbose=False):
    """Iterate through SDSS supernova and yield the SNCosmo input tables

    To return a select collection of band-passes, specify the band argument.
    No data cuts are applied to the returned data.

    Args:
        bands (iter[str]): Optional list of band-passes to return
        verbose    (bool): Optionally display progress bar while iterating

    Yields:
        An astropy table formatted for use with SNCosmo
    """

    iter_data = utils.build_pbar_iter(get_target_ids(), verbose)
    for id_val in iter_data:
        sncosmo_table = get_input_for_id(id_val, bands)
        if sncosmo_table:
            yield sncosmo_table
