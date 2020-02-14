#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

import numpy as np
import sncosmo
from astropy.io import ascii
from astropy.io import fits
from astropy.table import Table

from . import _meta as meta
from ... import _factory_funcs as factory
from ... import _utils as utils
from ...exceptions import InvalidObjId


@utils.require_data_path(meta.filter_path)
def register_filters(force=False):
    """Register filters for this survey / data release with SNCosmo

    Args:
        force (bool): Whether to re-register a band if already registered
    """

    data_arr = np.genfromtxt(meta.filter_path, skip_header=1)
    filt_table = Table(data_arr, names=['wave', 'u', 'g', 'r', 'i', 'z'])
    filt_table['wave'] *= 10  # Convert nm to angstroms

    # Bands are already registered in sncosmo under a different name.
    # We register them using the package standardized name
    for new_band_name in meta.band_names:
        built_in_name = new_band_name.split('_')[-1]

        # MEGACAMPSF are radius dependant
        if 'MEGACAMPSF' in built_in_name:
            trans = filt_table[built_in_name[-1].lower()]
            new_band = sncosmo.Bandpass(filt_table['wave'], trans)

        else:
            built_in_band = sncosmo.get_bandpass(built_in_name)
            new_band = sncosmo.Bandpass(built_in_band.wave, built_in_band.trans)

        new_band.name = new_band_name
        sncosmo.register(new_band, force=force)


@utils.require_data_path(meta.table_dir)
def get_available_tables():
    """Get table numbers for machine readable tables published in the paper
    for this data release"""

    dat_file_list = list(meta.table_dir.glob('table*.dat'))
    fits_file_list = list(meta.table_dir.glob('table*.fit'))
    file_list = dat_file_list + fits_file_list
    return sorted([str(f).rstrip('.datfit')[-2:] for f in file_list])


@utils.lru_copy_cache(maxsize=None)
@utils.require_data_path(meta.table_dir)
def load_table(table_id):
    """Load a table from the data paper for this survey / data

    See ``get_available_tables`` for a list of valid table IDs.

    Args:
        table_id (int, str): The published table number or table name
    """

    if table_id not in get_available_tables():
        raise ValueError(f'Table {table_id} is not available.')

    # Tables 2 is a fits file
    if table_id == 'f2':
        with fits.open(meta.table_dir / f'table{table_id}.fit') as hdulist:
            data = Table(hdulist[0].data)

        description = 'Covariance matrix of the binned distance modulus'
        data.meta['description'] = description
        return data

    # Remaining tables should be .dat files
    readme_path = meta.table_dir / 'ReadMe'
    table_path = meta.table_dir / f'table{table_id}.dat'
    if table_id not in get_available_tables():
        raise ValueError(f'Table {table_id} is not available.')

    data = ascii.read(str(table_path), format='cds', readme=str(readme_path))
    description_dict = utils.read_vizier_table_descriptions(readme_path)
    data.meta['description'] = description_dict[f'{table_id}']
    return data


@utils.require_data_path(meta.photometry_dir)
def get_available_ids():
    """Return a list of target object IDs for the current survey

    Returns:
        A list of object IDs as strings
    """

    file_list = meta.photometry_dir.glob('*.list')
    return sorted(str(f).split('-')[-1][:-5] for f in file_list)


@utils.require_data_path(meta.photometry_dir)
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

    # Get target meta data
    meta_data = dict()
    path = meta.photometry_dir / f'lc-{obj_id}.list'
    with open(path) as infile:
        line = infile.readline()
        while line.startswith('@'):
            split_line = line.lstrip('@').split(' ')
            meta_data[split_line[0]] = split_line[1].rstrip()
            line = infile.readline()

        # Initialize data as an astropy table
        names = ['Date', 'Flux', 'Fluxerr', 'ZP', 'Filter', 'MagSys']
        out_table = Table.read(
            infile.readlines(),
            names=names,
            comment='#|@',
            format='ascii.csv',
            delimiter=' ')

    # Set sncosmo format
    if format_table:
        out_table.rename_column('Date', 'time')
        out_table.rename_column('Flux', 'flux')
        out_table.rename_column('Fluxerr', 'fluxerr')
        out_table.rename_column('Filter', 'band')
        out_table.rename_column('ZP', 'zp')
        out_table.rename_column('MagSys', 'zpsys')

        out_table['time'] = utils.convert_to_jd(out_table['time'])
        out_table['band'] = ['jla_betoule14_' + b for b in out_table['band']]

    # Add package standard metadata
    ra = meta_data.pop('RA', None)
    dec = meta_data.pop('DEC', None)
    ra = float(ra) if ra is not None else ra
    dec = float(dec) if dec is not None else dec

    out_table.meta['obj_id'] = obj_id
    out_table.meta['ra'] = ra
    out_table.meta['dec'] = dec
    out_table.meta['z'] = float(meta_data.pop('Z_HELIO'))
    out_table.meta['z_err'] = None
    out_table.meta.update(meta_data)

    out_table.meta.pop('comments')
    out_table.meta.pop('SN')
    out_table.meta['comments'] = 'z represents the heliocentric redshift'

    return out_table


iter_data = factory.factory_iter_data(get_available_ids, get_data_for_id)
