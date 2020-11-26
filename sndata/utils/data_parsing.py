#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``data_parsing`` module provides general utilities related to parsing
data located on the local machine.
"""

import os
from pathlib import Path
from typing import Union

import numpy as np
import sncosmo
from astropy.table import Table

from . import unit_conversion
from ..exceptions import NoDownloadedData


def require_data_path(*data_dirs: Path):
    """Raise NoDownloadedData exception if given paths don't exist

    Args:
        *data_dirs: Path objects to check exists
    """

    for data_dir in data_dirs:
        if not data_dir.exists():
            raise NoDownloadedData()


def find_data_dir(survey_abbrev: str, release: str) -> Path:
    """Determine the directory where data files are stored for a data release

    If the directory does not exist, create it.

    Args:
        survey_abbrev: Abbreviation of the survey to load data for (e.g., CSP)
        release: Name of the data release from the survey (e.g., DR1)

    Returns:
        The path of the directory where
    """

    # Enforce the use of lowercase file names
    safe_survey = survey_abbrev.lower().replace(' ', '_')
    safe_release = release.lower().replace(' ', '_')

    # Default to using data directory specified in the environment
    if 'SNDATA_DIR' in os.environ:
        base_dir = Path(os.environ['SNDATA_DIR']).resolve()

    else:
        base_dir = Path(__file__).resolve().parent.parent / 'data'

    data_dir = base_dir / safe_survey / safe_release
    return data_dir


def parse_vizier_table_descriptions(readme_path: Union[Path, str]):
    """Returns the table descriptions from a vizier readme file

    Args:
        readme_path: Path of the file to read

    Returns:
        A dictionary {<Table number (int)>: <Table description (str)>}
    """

    table_descriptions = dict()
    with open(readme_path) as ofile:

        # Skip lines before table summary
        line = next(ofile)
        while line.strip() != 'File Summary:':
            line = next(ofile)

        # Skip table header
        for _ in range(5):
            line = next(ofile)

        # Iterate until end of table marker
        while not line.startswith('---'):
            line_list = line.split()
            table_num = line_list[0].lstrip('table').rstrip('.dat')
            if table_num.isdigit():
                table_num = int(table_num)

            table_desc = ' '.join(line_list[3:])
            line = next(ofile)

            # Keep building description for multiline descriptions
            while line.startswith(' '):
                table_desc += ' ' + line.strip()
                line = next(ofile)

            table_descriptions[table_num] = table_desc

    return table_descriptions


def parse_snoopy_path(path: str):
    """Return data from a snoopy file as an astropy table

    Args:
        path: The file path of a snoopy input file

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
        out_table.meta['ra'] = float(ra)
        out_table.meta['dec'] = float(dec)
        out_table.meta['z'] = float(z)
        out_table.meta['z_err'] = None

        # Read photometric data from the rest of the file
        band = None
        for line in ofile.readlines():
            line_list = line.split()
            if line.startswith('filter'):
                band = line_list[1]
                continue

            time, mag, mag_err = line_list
            out_table.add_row([time, band, mag, mag_err])

    out_table['time'] = unit_conversion.convert_to_jd(out_table['time'], format='snpy')
    return out_table


def read_csp_spectroscopy_file(path: str, format_table: bool = False) -> Table:
    """Read a file path of spectroscopic data from CSP

    Args:
        path: Path of file to read
        format_table: Format table to a sndata standard format

    Returns:
        An astropy table with file data and meta data
    """

    path = Path(path)
    obj_id = '20' + path.name.split('_')[0].lstrip('SN')

    # Handle the single file with a different data model:
    # This file has three columns instead of two
    if path.stem == 'SN07bc_070409_b01_BAA_IM':
        data = Table.read(path, format='ascii', names=['wavelength', 'flux', '_'])
        data.remove_column('_')

    else:
        data = Table.read(path, format='ascii', names=['wavelength', 'flux'])

    # Read the table meta data
    file_comments = data.meta['comments']
    redshift = float(file_comments[1].lstrip('Redshift: '))
    obs_date = float(file_comments[3].lstrip('JDate_of_observation: '))
    epoch = float(file_comments[4].lstrip('Epoch: '))

    # Add meta data to output table according to sndata standard
    data.meta['obj_id'] = obj_id
    data.meta['ra'] = None
    data.meta['dec'] = None
    data.meta['z'] = redshift
    data.meta['z_err'] = None
    del data.meta['comments']

    data['time'] = obs_date
    if format_table:
        # Add remaining columns. These values are constant for a single file
        # (i.e. a single spectrum) but vary across files (across spectra)
        _, _, w_range, telescope, instrument = path.stem.split('_')
        data['epoch'] = epoch
        data['wavelength_range'] = w_range
        data['telescope'] = telescope
        data['instrument'] = instrument

        # Enforce an intuitive column order
        data = data[[
            'time', 'wavelength', 'flux', 'epoch',
            'wavelength_range', 'telescope', 'instrument']]

    return data


def register_filter_file(file_path: str, filter_name: str, force: bool = False):
    """Registers filter profiles with sncosmo if not already registered

    Assumes the file at ``file_path`` is a two column, white space delimited
    ascii table.

    Args:
        file_path: Path of ascii table with wavelength (Ang) and transmission
        filter_name: The name of the registered filter.
        force: Whether to re-register a band if already registered
    """

    # Get set of registered builtin and custom band passes
    available_bands = set(
        k[0] for k in sncosmo.bandpasses._BANDPASSES._loaders)

    available_bands.update(
        k[0] for k in sncosmo.bandpasses._BANDPASSES._instances)

    # Register the new bandpass
    if filter_name not in available_bands:
        wave, trans = np.genfromtxt(file_path).T
        is_good_data = ~np.isnan(wave) & ~np.isnan(trans)
        band = sncosmo.Bandpass(wave[is_good_data], trans[is_good_data])
        band.name = filter_name
        sncosmo.register(band, force=force)
