#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides utilities used by various submodules."""

import shutil
import tarfile
from functools import wraps
from pathlib import Path, PosixPath
from tempfile import TemporaryFile

import requests
from tqdm import tqdm


class NoDownloadedData(Exception):
    def __init__(self, *args, **kwargs):
        default_message = \
            'Data has not been downloaded for this module / data release.'

        if not (args or kwargs):
            args = (default_message,)

        super().__init__(*args, **kwargs)


def require_data_path(data_dir):
    """Function decorator to raise NoDownloadedData exception if
       the path ``data_dir`` does not exist

    Args:
        data_dir (Path): Path object to check for
    """

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not data_dir.exists():
                raise NoDownloadedData()

            return func(*args, **kwargs)

        return wrapper

    return inner


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


def factory_iter_data(id_func, data_func):
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

        iterable = build_pbar(id_func(), verbose)
        for obj_id in iterable:
            data_table = data_func(obj_id, format_sncosmo=format_sncosmo)
            if filter_func(data_table):
                yield data_table

    return iter_data


def factory_delete_module_data(data_dir):
    def delete_module_data():
        """Delete any data for the current survey / data release"""

        try:
            shutil.rmtree(data_dir)

        except FileNotFoundError:
            pass

    return delete_module_data
