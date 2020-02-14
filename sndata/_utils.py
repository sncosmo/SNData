#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides utilities used by various submodules."""

import functools
import os
import tarfile
from copy import deepcopy
from functools import wraps
from pathlib import Path, PosixPath
from tempfile import TemporaryFile
from warnings import warn

import numpy as np
import requests
from tqdm import tqdm

from .exceptions import NoDownloadedData


def lru_copy_cache(maxsize=128, typed=False, copy=True):
    """Decorator to cache the return of a function

    Similar to ``functools.lru_cache``, but allows a copy of the cached value
    to be returned, thus preventing mutation of the cache.

    Args:
        maxsize (int): Maximum size of the cache
        typed  (bool): Cache objects of different types separately
        copy   (bool): Return a copy of the cached item

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


@np.vectorize
def convert_to_jd(date):
    """Convert MJD and Snoopy dates into JD

    Args:
        date (float): Time stamp in JD, MJD, or SNPY format

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


def check_url(url, timeout=None):
    """Return whether a connection can be established to a given URL

    If False, a warning is also raised.

    Args:
        url     (str): The URL to check
        timeout (int): Optional number of seconds to timeout after

    Returns:
        A boolean
    """

    try:
        _ = requests.get(url, timeout=timeout)
        return True

    except requests.ConnectionError:
        warn(f'Could not connect to {url}')

    return False


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

    is_file_handle = not isinstance(out_file, (str, PosixPath))
    if not is_file_handle:
        Path(out_file).parent.mkdir(parents=True, exist_ok=True)
        out_file = open(out_file, 'wb')

    out_file.write(response.content)

    if not is_file_handle:
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


def require_data_path(*data_dirs):
    """Decorator to raise NoDownloadedData exception if given paths don't exist

    Args:
        *data_dirs (Path): Path objects to check exists
    """

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for data_dir in data_dirs:
                if not data_dir.exists():
                    raise NoDownloadedData()

            return func(*args, **kwargs)

        return wrapper

    return inner


def read_vizier_table_descriptions(readme_path):
    """Returns the table descriptions from a vizier readme file

    Args:
        readme_path (str): Path of the file to read

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


def create_data_dir(survey_name, release):
    """Create the data directory for a given survey and release

    Directories are created in ``environ['SNDATA_DIR']`` using lowercase names
    and underscores instead of spaces.

    Args:
        survey_name (str): The name of a survey (e.g., csp)
        release     (str): The name of a data release from the survey (e.g., dr3)

    Returns:
        A Path object representing the created directory
    """

    safe_survey = survey_name.lower().replace(' ', '_')
    safe_release = release.lower().replace(' ', '_')
    path = Path(os.environ['SNDATA_DIR']).resolve() / safe_survey / safe_release
    path.mkdir(parents=True, exist_ok=True)
    return path
