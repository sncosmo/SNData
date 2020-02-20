#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides general utilities."""

import functools
import logging
import os
import tarfile
from copy import deepcopy
from pathlib import Path, PosixPath
from tempfile import TemporaryFile
from typing import Union
from warnings import warn

import numpy as np
import requests
import sncosmo
from astropy.coordinates import Angle
from tqdm import tqdm

from .exceptions import NoDownloadedData

log = logging.getLogger(__name__)


def hourangle_to_degrees(
        rah: float,
        ram: float,
        ras: float,
        dec_sign: str,
        decd: float,
        decm: float,
        decs: float) -> (float, float):
    """Convert from hour angle to degrees

    Args:
        rah: RA hours
        ram: RA arcminutes
        ras: RA arcseconds
        dec_sign: Sign of the declination ('+' or '-')
        decd: Dec degrees
        decm: Dec arcmin
        decs: Dec arcsec
    """

    # Convert Right Ascension
    ra = Angle((rah, ram, ras), unit='hourangle').to('deg').value

    # Convert Declination
    sign = -1 if dec_sign == '-' else 1
    dec = (
            sign * decd +  # Already in degrees
            decm / 60 +  # arcmin to degrees
            decs / 60 / 60  # arcesc to degrees
    )
    return ra, dec


def find_and_create_data_dir(survey_abbrev: str, release: str) -> Path:
    """Determine the directory where data files are stored for a data release

    If the directory does not exist, create it.

    Args:
        survey_abbrev: Abbreviation of the survey to load data for (e.g., CSP)
        release: Name of the data release from the survey (e.g., DR1)

    Returns:
        The path of the directory where
    """

    safe_survey = survey_abbrev.lower().replace(' ', '_')
    safe_release = release.lower().replace(' ', '_')

    if 'SNDATA_DIR' in os.environ:
        base_dir = Path(os.environ['SNDATA_DIR']).resolve()

    else:
        base_dir = Path(__file__).resolve().parent / 'data'

    data_dir = base_dir / safe_survey / safe_release
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def lru_copy_cache(maxsize: int = 128, typed: bool = False, copy: bool = True):
    """Decorator to cache the return of a function

    Similar to ``functools.lru_cache``, but allows a copy of the cached value
    to be returned, thus preventing mutation of the cache.

    Args:
        maxsize: Maximum size of the cache
        typed: Cache objects of different types separately (Default: False)
        copy: Return a copy of the cached item (Default: True)

    Returns:
        A decorator
    """

    if not copy:
        return functools.lru_cache(maxsize, typed)

    def decorator(f):
        cached_func = functools.lru_cache(maxsize, typed)(f)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return deepcopy(cached_func(*args, **kwargs))

        return wrapper

    return decorator


def build_pbar(data: iter, verbose: Union[bool, dict]):
    """Cast an iterable into a progress bar

    If verbose is False, return ``data`` unchanged.

    Args:
        data: An iterable object
        verbose: Arguments for tqdm.tqdm
    """

    if isinstance(verbose, dict):
        iter_data = tqdm(data, **verbose)

    elif verbose:
        iter_data = tqdm(data)

    else:
        iter_data = data

    return iter_data


@np.vectorize
def convert_to_jd(date: float):
    """Convert MJD and Snoopy dates into JD

    Args:
        date: Time stamp in JD, MJD, or SNPY format

    Returns:
        The time value in JD format
    """

    snoopy_offset = 53000
    mjd_offset = 2400000.5

    if date < snoopy_offset:
        date += snoopy_offset

    if date < mjd_offset:
        date += mjd_offset

    return date


def check_url(url: str, timeout: int = None):
    """Return whether a connection can be established to a given URL

    If False, a warning is also raised.

    Args:
        url: The URL to check
        timeout: Optional number of seconds to timeout after

    Returns:
        A boolean
    """

    try:
        _ = requests.get(url, timeout=timeout)
        return True

    except requests.ConnectionError:
        warn(f'Could not connect to {url}')

    return False


def download_file(url: str, out_file: str):
    """Download data to a file

    Args:
        url: URL of the file to download
        out_file: The file path to write to or a file object
    """

    log.info(f'Fetching {url}')

    # Establish remote connection
    response = requests.get(url)
    response.raise_for_status()

    is_file_handle = not isinstance(out_file, (str, PosixPath))
    if not is_file_handle:
        Path(out_file).parent.mkdir(parents=True, exist_ok=True)
        out_file = open(out_file, 'wb')

    out_file.write(response.content)

    if not is_file_handle:
        out_file.close()


def download_tar(url: str, out_dir: str, mode: str = None):
    """Download and unzip a .tar.gz file to a given output path

    Args:
        url: URL of the file to download
        out_dir: The directory to unzip file contents to
        mode: Compression mode (Default: r:gz)
    """

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Download data to file and decompress
    with TemporaryFile() as ofile:
        download_file(url, ofile)

        # Writing to the file moves us to the end of the file
        # We move back to the beginning so we can decompress the data
        ofile.seek(0)

        with tarfile.open(fileobj=ofile, mode=mode) as data:
            for file_ in data:
                try:
                    data.extract(file_, path=out_dir)

                except IOError:
                    # If output path already exists, delete it and try again
                    (out_dir / file_.name).unlink()
                    data.extract(file_, path=out_dir)


def require_data_path(*data_dirs: Path):
    """Raise NoDownloadedData exception if given paths don't exist

    Args:
        *data_dirs: Path objects to check exists
    """

    for data_dir in data_dirs:
        if not data_dir.exists():
            raise NoDownloadedData()


def read_vizier_table_descriptions(readme_path: Union[Path, str]):
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


def register_filter(file_path: str, filter_name: str, force: bool = False):
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
        filter_data = np.genfromtxt(file_path).T
        band = sncosmo.Bandpass(filter_data[0], filter_data[1])
        band.name = filter_name
        sncosmo.register(band, force=force)
