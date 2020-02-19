#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the base class of the data access API."""

import os
import shutil
from pathlib import Path
from typing import List, Union

import numpy as np
from astropy.table import Table

from . import _utils as utils
from .exceptions import InvalidObjId


class DataRelease:
    """Base class for enforcing a standard API"""

    @classmethod
    def _find_or_create_data_dir(cls):
        """Define and create a directory to store downloaded data files"""

        safe_survey = cls.survey_abbrev.lower().replace(' ', '_')
        safe_release = cls.release.lower().replace(' ', '_')

        if 'SNDATA_DIR' in os.environ:
            base_dir = Path(os.environ['SNDATA_DIR']).resolve()

        else:
            base_dir = Path(__file__).resolve().parent / 'data'

        cls.data_dir = base_dir / safe_survey / safe_release
        cls.data_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_zp_for_band(cls, band: str):
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
            force: Re-register a band if already registered (Default: False)
        """

        for _file_name, _band_name in zip(
                self._filter_file_names, self.band_names):
            filter_path = self.filter_dir / _file_name
            utils.register_filter(filter_path, _band_name, force=force)

    def get_available_tables(self) -> List[Union[str, int]]:
        """Get available Ids for tables published by the paper for this data
        release"""

        return self._get_available_tables()

    @utils.lru_copy_cache(maxsize=None)
    def load_table(self, table_id: Union[int, str]) -> Table:
        """Return a table from the data paper for this survey / data

        See ``get_available_tables`` for a list of valid table IDs.

        Args:
            table_id: The published table number or table name
        """

        return self._load_table(table_id)

    def get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey

        Returns:
            A list of object IDs as strings
        """

        return self._get_available_ids()

    def get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        See ``get_available_ids()`` for a list of available ID values.

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        if obj_id not in self.get_available_ids():
            raise InvalidObjId()

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
            shutil.rmtree(self.data_dir)

        except FileNotFoundError:
            pass
