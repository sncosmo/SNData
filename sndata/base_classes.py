#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``base_classes`` module defines parent classes used by the data access
API to define basic data handling and to enforce a consistent user interface.
For an example on how to use these classes to create custom data access module
for a new survey / data release, see the :ref:`CustomClasses` section of the
docs.
"""

import functools
import shutil
import warnings
from typing import List
from typing import Union

import numpy as np
from astropy.io import ascii
from astropy.table import Table

from . import utils
from .exceptions import InvalidObjId, InvalidTableId

# Define short hand type for Ids of Vizier Tables
VizierTableId = Union[int, str]


def ignore_warnings_wrapper(func: callable) -> callable:
    """Ignores warnings issued by the wrapped function call"""

    @functools.wraps(func)
    def inner(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            return func(*args, **kwargs)

    return inner


class DefaultParser:
    """Prebuilt data parsing tools for Vizier tables and photometric filters

    For more information see the :ref:`CustomClasses` section of the docs.
    """

    def _get_available_tables(self) -> List[VizierTableId]:
        """Default backend functionality of ``get_available_tables`` function"""

        # Find available tables - assume standard Vizier naming scheme
        # This includes assuming lowercase file names
        table_nums = []
        for f in self._table_dir.rglob('table*.dat'):
            table_number = f.stem.lstrip('table')
            try:
                table_number = int(table_number)

            except ValueError:
                pass

            table_nums.append(table_number)

        return sorted(table_nums, key=str)

    def _load_table(self, table_id: VizierTableId) -> Table:
        """Default backend functionality of ``load_table`` function"""

        readme_path = self._table_dir / 'ReadMe'
        table_path = self._table_dir / f'table{table_id}.dat'

        # Read data from file and add meta data from the readme
        data = ascii.read(str(table_path), format='cds', readme=str(readme_path))
        description = utils.read_vizier_table_descriptions(readme_path)[table_id]
        data.meta['description'] = description
        return data

    def _register_filters(self, force: bool = False):
        """Default backend functionality of ``register_filters`` function"""

        bandpass_data = zip(self._filter_file_names, self.band_names)
        for _file_name, _band_name in bandpass_data:
            filter_path = self._filter_dir / _file_name
            utils.register_filter_file(filter_path, _band_name, force=force)


class SpectroscopicRelease:
    """Generic representation of a spectroscopic data release

    This class is a template designed to enforce a consistent user interface
    and requires child classes to fill in incomplete functionality.
    """

    # General metadata
    publications = tuple()
    ads_url = None
    survey_name = None
    survey_abbrev = None
    release = None
    survey_url = None
    data_type = 'spectroscopic'

    def __init__(self, survey_abbrev: str = None, release: str = None):
        """Represent Vizier data downloaded on the local machine

        Args:
            survey_abbrev: Abbreviation of the survey to load data for (e.g., CSP)
            release: Name of the data release from the survey (e.g., DR1)
        """

        err_msg = '``{}`` must either be passed at initialization or set as attribute'
        if survey_abbrev is None and not hasattr(self, 'survey_abbrev'):
            raise ValueError(err_msg.format('survey_abbrev'))

        if release is None and not hasattr(self, 'release'):
            raise ValueError(err_msg.format('release'))

        self.survey_abbrev = survey_abbrev if survey_abbrev else self.survey_abbrev
        self.release = release if release else self.release

        self._data_dir = utils.find_data_dir(self.survey_abbrev, self.release)
        self._table_dir = self._data_dir / 'tables'

    def get_available_tables(self) -> List[VizierTableId]:
        """Get Ids for available vizier tables published by this data release"""

        # Raise error if data is not downloaded
        utils.require_data_path(self._data_dir)
        return self._get_available_tables()

    @utils.lru_copy_cache(maxsize=None)
    @ignore_warnings_wrapper
    def load_table(self, table_id: VizierTableId) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        # Raise error if data is not downloaded
        if table_id not in self.get_available_tables():
            raise InvalidTableId(f'Table {table_id} is not available.')

        return self._load_table(table_id)

    def get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey

        Returns:
            A list of object IDs as strings
        """

        utils.require_data_path(self._data_dir)
        return self._get_available_ids()

    @ignore_warnings_wrapper
    def get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        See ``get_available_ids()`` for a list of available ID values.

        Args:
            obj_id: The ID of the desired object
            format_table: Format data into the ``sndata`` standard format

        Returns:
            An astropy table of data for the given ID
        """

        if obj_id not in self.get_available_ids():
            raise InvalidObjId(f'Object Id not available: {obj_id}')

        return self._get_data_for_id(obj_id, format_table)

    def iter_data(
            self,
            verbose: bool = False,
            format_table: bool = True,
            filter_func: bool = None) -> Table:
        """Iterate through all available targets and yield data tables

        An optional progress bar can be formatted by passing a dictionary of
        ``tqdm`` arguments. Outputs can be optionally filtered by passing a
        function ``filter_func`` that accepts a data table and returns a
        boolean.

        Args:
            verbose: Optionally display progress bar while iterating
            format_table: Format data for ``SNCosmo`` (Default: True)
            filter_func: An optional function to filter outputs by

        Yields:
            Astropy tables
        """

        # Default to returning only non-empty tables
        if filter_func is None:
            filter_func = lambda x: x

        iterable = utils.build_pbar(self.get_available_ids(), verbose)
        for obj_id in iterable:
            data_table = self.get_data_for_id(
                obj_id, format_table=format_table)

            if filter_func(data_table):
                yield data_table

    def delete_module_data(self):
        """Delete any data for the current survey / data release"""

        try:
            shutil.rmtree(self._data_dir)

        except FileNotFoundError:
            pass

    def download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        if not hasattr(self, '_download_module_data'):
            raise RuntimeError(
                'This data set does not support downloading remote data')

        self._download_module_data(force, timeout)

    def __repr__(self):
        # Using self.__class__ ensures correct name appears for child classes
        class_name = self.__class__.__name__
        return f'<{class_name} ({self.survey_abbrev} {self.release})>'


# noinspection PyUnresolvedReferences
class PhotometricRelease(SpectroscopicRelease):
    """Generic representation of a photometric data release

    This class is a template designed to enforce a consistent user interface
    and requires child classes to fill in incomplete functionality.
    """

    data_type = 'photometric'

    # Photometric metadata
    @property
    def band_names(self) -> tuple:
        raise NotImplementedError('Band passes are not defined for this survey')

    @property
    def zero_point(self) -> tuple:
        raise NotImplementedError('Zero points are not defined for this survey')

    @classmethod
    def get_zp_for_band(cls, band: str) -> str:
        """Get the zeropoint for a given band name

        Args:
            band: The name of the bandpass
        """

        sorter = np.argsort(cls.band_names)
        indices = np.searchsorted(cls.band_names, band, sorter=sorter)
        return np.array(cls.zero_point)[sorter[indices]]

    def register_filters(self, force: bool = False):
        """Register filters for this survey / data release with SNCosmo

        Args:
            force: Re-register a band if already registered
        """

        utils.require_data_path(self._data_dir)
        self._register_filters(force)
