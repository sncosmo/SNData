#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

from astropy.table import Table, vstack

from .. import sako18
from ..sako18 import _meta as meta
from ... import _utils as utils

# Cache the master table for later use
_photometry_master_table = None

get_available_tables = sako18.get_available_tables
load_table = sako18.load_table


def register_filters(force=False):
    """Register filters for this survey / data release with SNCosmo

    Args:
        force (bool): Whether to re-register a band if already registered
    """

    raise ValueError('The ``sako18spec`` module is a spectroscopic data '
                     'release and has no filters to register. '
                     'See the ``sako18`` module for photometric data')


@utils.require_data_path(meta.spectra_dir)
def get_available_ids():
    """Return a list of target object IDs for the current survey

    Returns:
        A list of object IDs as strings
    """

    files = meta.spectra_dir.glob('*.txt')
    return sorted(set(f.stem.split('-')[0].strip('sngal') for f in files))


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

    master_table = load_table('master')
    spectra_summary = load_table(9)

    # Read in all spectra for the given object Id
    data_tables = []
    for path in meta.spectra_dir.glob(f'*{obj_id}-*.txt'):
        data = Table.read(path, format='ascii', names=['wavelength', 'flux'])

        # Get meta data for the current spectrum from the summary table
        sid = path.stem.split('-')[-1]
        master_row = spectra_summary[spectra_summary['SID'] == sid]
        assert len(master_row) == 1

        data['spec_type'] = path.stem.split('-')[0].strip(obj_id)
        data['date'] = master_row['Date'][0]
        data['telescope'] = master_row['Telescope'][0]
        data_tables.append(data)

    # Load target meta data from the master table of the photometric data
    phot_record_idx = master_table['CID'] == int(obj_id)
    phot_record = master_table[phot_record_idx]

    out_data = vstack(data_tables)
    out_data.meta['obj_id'] = obj_id

    if phot_record:
        out_data.meta['ra'] = phot_record['RA'][0]
        out_data.meta['dec'] = phot_record['DEC'][0]
        out_data.meta['z'] = phot_record['zCMB'][0]
        out_data.meta['z_err'] = phot_record['zerrCMB'][0]

    else:
        out_data.meta['ra'] = None
        out_data.meta['dec'] = None
        out_data.meta['z'] = None
        out_data.meta['z_err'] = None

    out_data.meta['dtype'] = 'spectroscopic'
    out_data.meta['comments'] = \
        'z represents CMB corrected redshift of the supernova.'

    return out_data


iter_data = utils.factory_iter_data(get_available_ids, get_data_for_id)
