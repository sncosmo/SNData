#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Utilities for interfacing with external services."""

import json

import numpy as np
import pandas as pd
import requests
import sncosmo
from astropy.table import Table


def add_sn_prefix(uia_name):
    """Add the SN prefix to an IAU name if not already present

    Args:
        uia_name (str): SN name (e.g. '2011fe')
    """

    if not uia_name.lower().startswith('sn'):
        uia_name = "SN" + uia_name

    return uia_name


def query_ned_coords(uia_name):
    """Return the J2000 RA and Dec for UIA named supernovae from NED

    Args:
        uia_name (str): SN name (e.g. '2011fe')

    Returns:
        RA position in degrees
        Dec position in degrees
    """

    uia_name = add_sn_prefix(uia_name)

    url = (
        f"http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname={uia_name}"
        "&out_csys=Equatorial"
        "&out_equinox=J2000.0"
        "&of=ascii_bar"
        "&list_limit=5"
        "&img_stamp=NO"
    )

    response = requests.get(url)
    response.raise_for_status()

    obj_data = response.content.decode('utf-8').split('\n')[-2].split('|')
    if obj_data[0] != '1':
        raise RuntimeError(f"Could not retrieve coordinates for {uia_name}")

    return float(obj_data[2]), float(obj_data[3])


def _query_osc(uia_name, data_type=None):
    """Query various types of data from the Open Supernova Catalog

    Args:
        uia_name     (str): SN name (e.g. '2011fe')
        data_type    (str): The type of data to query (r.g. 'Photometry')

    Returns:
        A dictionary of queried data
    """

    # Construct URL
    uia_name = add_sn_prefix(uia_name)
    url = f'https://api.astrocats.space/{uia_name}/'
    if data_type:
        url += f'{data_type}/'

    response = requests.get(url)
    response.raise_for_status()
    data = json.loads(response.content.decode('utf-8'))[uia_name]
    return data[data_type] if data_type else data


def query_osc(uia_name):
    """Query meta data from the Open Supernova Catalog

    Args:
         uia_name (str): SN name (e.g. '2011fe')

    Returns:
        A dictionary of meta data for the specified object
    """

    return _query_osc(uia_name)


def query_osc_photometry(uia_name):
    """Return photometric data from the Open Supernova Catalog

    Args:
        uia_name     (str): SN name (e.g. '2011fe')

    Returns:
        An astropy table of photometric data from the OSC
    """

    data = Table.from_pandas(pd.DataFrame(_query_osc(uia_name, 'photometry')))
    data.meta = _query_osc(uia_name)
    return data


def query_osc_spectra(uia_name):
    """Return photometric data from the Open Supernova Catalog

    Args:
        uia_name     (str): SN name (e.g. '2011fe')

    Returns:
        A list of spectral data as dictionaries
    """

    return _query_osc(uia_name, 'spectra')


def parse_snoopy_data(path):
    """Return data from a snoopy file as an astropy table

    Args:
        path (str): The file path of a snoopy input file

    Returns:
        An astropy table with columns 'time', 'band', 'mag', and 'mag_err'
    """

    out_table = Table(
        names=['time', 'band', 'mag', 'mag_err'],
        dtype=[float, object, float, float]
    )

    with open(path) as ofile:
        # Get meta data from first line
        name, z, ra, dec = ofile.readline().split()
        out_table.meta['obj_id'] = name
        out_table.meta['redshift'] = float(z)
        out_table.meta['ra'] = float(ra)
        out_table.meta['dec'] = float(dec)

        # Read photometric data from the rest of the file
        band = None
        for line in ofile.readlines():
            line_list = line.split()
            if line.startswith('filter'):
                band = line_list[1]
                continue

            time, mag, mag_err = line_list
            out_table.add_row([time, band, mag, mag_err])

    out_table['time'] += 53000  # Convert from snoopy format to MJD
    return out_table


def register_filter(file_path, filt_name, force=False):
    """Registers filter profiles with sncosmo if not already registered

    Args:
        file_path (str): Path of an ascii table with wavelength (Angstrom)
                          and transmission columns
        filt_name (str): The name of the registered filter.
        force    (bool): Whether to re-register a band if already registered
    """

    # Get set of registered builtin and custom band passes
    available_bands = set(
        k[0] for k in sncosmo.bandpasses._BANDPASSES._loaders)
    available_bands.update(
        k[0] for k in sncosmo.bandpasses._BANDPASSES._instances)

    # Register the new bandpass
    if filt_name not in available_bands:
        filt_data = np.genfromtxt(file_path).T
        band = sncosmo.Bandpass(filt_data[0], filt_data[1])
        band.name = filt_name
        sncosmo.register(band, force=force)
