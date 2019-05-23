#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides utilities used by various submodules."""

import tarfile
from pathlib import Path, PosixPath
from tempfile import TemporaryFile

import numpy as np
import requests
import sncosmo
from astropy.table import Table
from tqdm import tqdm


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
        out_table.meta['name'] = name
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

    return out_table


def register_filter(file_path, filt_name):
    """Registers filter profiles with sncosmo if not already registered

    Args:
        file_path (str): Path of an ascii table with wavelength (Angstrom)
                          and transmission columns
        filt_name (str): The name of the registered filter.
    """

    # Get set of registered builtin and custom bandpasses
    available_bands = set(
        k[0] for k in sncosmo.bandpasses._BANDPASSES._loaders)
    available_bands.update(
        k[0] for k in sncosmo.bandpasses._BANDPASSES._instances)

    # Register the new bandpass
    if filt_name not in available_bands:
        filt_data = np.genfromtxt(file_path).T
        band = sncosmo.Bandpass(filt_data[0], filt_data[1])
        sncosmo.register(band, filt_name, force=False)


def download_file(url, out_file):
    """Download data to a file

    Args:
        url      (str): URL of the file to download
        out_file (str): The file path to write to or a file object
    """

    print(f'Fetching {url}')

    # Establish remote connection
    response = requests.get(url)
    response.raise_for_status()

    close_on_exit = isinstance(out_file, (str, PosixPath))
    if close_on_exit:
        Path(out_file).parent.mkdir(parents=True, exist_ok=True)
        out_file = open(out_file, 'wb')

    out_file.write(response.content)

    if close_on_exit:
        out_file.close()


def download_tar(url, out_dir, mode=None):
    """Download and unzip a .tar.gz file to a given output path

    Args:
        url     (str): URL of the file to download
        out_dir (str): The directory to unzip file contents to
        mode    (str): Compression mode (Default: r:gz)
    """

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Establish remote connection
    response = requests.get(url)
    response.raise_for_status()

    # Download data to file and decompress
    with TemporaryFile() as ofile:
        download_file(url, ofile)

        ofile.seek(0)
        with tarfile.open(fileobj=ofile, mode=mode) as data:
            data.extractall(out_dir)


def build_pbar(data, verbose):
    """Cast an iterable into a progress bar

    If verbose is False, return ``data`` unchanged.

    Args:
        data          (iter): An iterable object
        verbose (bool, dict): Arguments for tqdm.tqdm
    """

    if isinstance(verbose, dict):
        iter_data = tqdm(data, **verbose)

    elif verbose:
        iter_data = tqdm(data)

    else:
        iter_data = data

    return iter_data
