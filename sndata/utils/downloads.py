#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``downloads`` module supports downloading data files in various file
formats.
"""

import sys
import tarfile
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import IO, Union

import requests
from tqdm import tqdm


def download_file(
        url: str,
        destination: Union[str, Path, IO] = None,
        force: bool = False,
        timeout: float = 15,
        verbose: bool = True):
    """Download content from a url to a file

    If ``destination`` is a path but already exists, skip the
    download unless ``force`` is also ``True``.

    Args:
        url: URL of the file to download
        destination: Path or file object to download to
        force: Re-Download locally available data (Default: False)
        timeout: Seconds before raising timeout error (Default: 15)
        verbose: Print status to stdout
    """

    destination_is_path = isinstance(destination, (str, Path))
    if destination_is_path:
        path = Path(destination)
        if (not force) and path.exists():
            return

        path.parent.mkdir(exist_ok=True, parents=True)
        destination = path.open('wb')

    if verbose:
        tqdm.write(f'Fetching {url}', file=sys.stdout)
        response = requests.get(url, stream=True, timeout=timeout)
        response.raise_for_status()

        total = int(response.headers.get('content-length', 0))
        chunk_size = 1024
        with tqdm(total=total, unit='B', unit_scale=True, unit_divisor=chunk_size, file=sys.stdout) as pbar:
            for data in response.iter_content(chunk_size=chunk_size):
                pbar.update(destination.write(data))

    else:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        destination.write(response.content)
        destination.write(response.content)

    if destination_is_path:
        destination.close()


def download_tar(
        url: str,
        out_dir: str,
        mode: str = 'r:gz',
        force: bool = False,
        timeout: float = 15,
        skip_exists: str = None
):
    """Download and unzip a .tar.gz file to a given output directory

    Args:
        url: URL of the file to download
        out_dir: The directory to unzip file contents to
        mode: Compression mode (Default: r:gz)
        force: Re-Download locally available data (Default: False)
        timeout: Seconds before raising timeout error (Default: 15)
        skip_exists: Optionally skip the download if given path exists
    """

    out_dir = Path(out_dir)

    # Skip download if file already exists or url unavailable
    if skip_exists and Path(skip_exists).exists() and not force:
        return

    # Download data to file and decompress
    with NamedTemporaryFile() as temp_file:
        download_file(url, destination=temp_file, timeout=timeout)

        # Writing to the file moves us to the end of the file
        # We move back to the beginning so we can decompress the data
        temp_file.seek(0)

        out_dir.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=temp_file, mode=mode) as data_archive:
            for ffile in data_archive:
                try:
                    data_archive.extract(ffile, path=out_dir)

                except IOError:
                    # If output path already exists, delete it and try again
                    (out_dir / ffile.name).unlink()
                    data_archive.extract(ffile, path=out_dir)
