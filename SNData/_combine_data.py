#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

"""This module handles combining data from different data sets."""

import pandas as pd
from astropy.table import Table

from . import _utils as utils


class Combined_Dataset:

    def __init__(self, *data_sets):
        """Combine data from different surveys into a single data set"""

        self._data_modules = set(*data_sets)

        # Create a DataFrame of combined object ids
        self._obj_ids = None
        for data_module in self._data_modules:
            _, survey, release = data_module.__name__.split('.')
            id_df = pd.DataFrame({'obj_id': data_module.get_available_ids()})
            id_df.insert(1, 'flag', 1)
            id_df.insert(0, 'release', release)
            id_df.insert(0, 'survey', survey)

            if self._obj_ids is None:
                self._obj_ids = id_df

            else:
                self._obj_ids.append(id_df, ignore_index=True)

    def download_combined_data(self, force=False):
        """Download data for all combined surveys / data releases

        Args:
            force (bool): Re-Download locally available data (Default: False)
        """

        for module in self._data_modules:
            print(f'Downloading data for {module.__name__}')
            module.download_module_data(force=force)

    def delete_combined_data(self):
        """Delete any data for all combined surveys / data releases"""

        for module in self._data_modules:
            module.delete_module_data()

    def get_available_ids(self):
        """Return a table of object ids available in the combined data set"""

        id_table = Table.from_pandas(self._obj_ids)
        id_table['ignore'] = 1 - id_table['flag']
        id_table.remove_column('flag')
        return id_table

    def get_duplicate_ids(self, ignore_survey=True, ignore_release=True):
        """Return a table of duplicate object ids for the combined data set

        Args:
            ignore_survey  (bool): Don't report ids from different surveys (Default: True)
            ignore_release (bool): Don't report ids from different releases (Default: True)

        Returns:
            An astropy table of duplicate id values
        """

        subset = ['obj_id']
        if not ignore_survey:
            subset.append('survey')

        if not ignore_release:
            subset.append('release')

        indices = self._obj_ids.duplicated(subset=subset, keep=False)
        return Table.from_pandas(self._obj_ids[indices])

    def register_filters(self, force=False):
        """Register filters for the combined data with SNCosmo

        Args:
            force (bool): Whether to re-register a band if already registered (Default: False)
        """

        for module in self._data_modules:
            try:
                module.register_filters(force=force)

            except utils.NoDownloadedData:
                raise utils.NoDownloadedData(
                    f'No data downloaded for {module.__name__}')

    def get_data_for_id(self, obj_id, survey=None, release=None,
                        format_sncosmo=False):
        """Returns data for a given object id

        See ``get_available_ids()`` for a table of available id values.

        Args:
            obj_id          (str): The ID of the desired object
            survey          (str): The name of the object's survey (Default: None)
            release         (str): The name of the object's data release (Default: None)
            format_sncosmo (bool): Format data for SNCosmo.fit_lc (Default: False)

        Returns:
            An astropy table of data for the given ID
        """

        pass

    def iter_data(self, survey=None, release=None, verbose=False,
                  format_sncosmo=False, filter_func=None):
        """Iterate through all available targets and yield data tables

        An optional progress bar can be formatted by passing a dictionary of tqdm
        arguments. Outputs can be optionally filtered by passing a function
        ``filter_func`` that accepts a data table and returns a boolean.

        Args:
            survey          (str): Only include data from a given survey (Default: None)
            release         (str): Only include data from a given data release (Default: None)
            verbose  (bool, dict): Optionally display progress bar while iterating (Default: False)
            format_sncosmo (bool): Format data for SNCosmo.fit_lc (Default: False)
            filter_func    (func): An optional function to filter outputs by

        Yields:
            Astropy tables
        """

        pass

    def map_object_ids(self, mapping):
        """Manually rename an object's id

        Object ids should be specified as a tuple
        (survey name, release name, obj_id value).

        Args:
            mapping (dict): A dictionary of the form {<old id>: <new id>, ...}
        """

        pass

    def ignore_id(self, obj_id, survey=None, release=None):
        """Flag an object id to be ignored

        Args:
            obj_id  (str): The ID of the desired object
            survey  (str): The name of the object's survey (Default: None)
            release (str): The name of the object's data release (Default: None)
        """

        pass
