#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

"""This module handles combining data from different data sets."""

import pandas as pd

from . import _utils as utils


# Todo: Class Docstring
# Todo: Implement ID joining
class CombinedDataset:

    def __init__(self, *data_sets):
        """Combine data from different surveys into a single data set"""

        self._data_modules = dict()

        # Create a DataFrame of combined object ids
        self._obj_ids = None
        for data_module in set(data_sets):
            _, survey, release = data_module.__name__.split('.')
            id_df = pd.DataFrame({'obj_id': data_module.get_available_ids()})
            id_df.insert(0, 'release', release)
            id_df.insert(0, 'survey', survey)

            self._data_modules[':'.join((survey, release))] = data_module

            if self._obj_ids is None:
                self._obj_ids = id_df

            else:
                self._obj_ids.append(id_df, ignore_index=True)

    def download_module_data(self, force=False):
        """Download data for all combined surveys / data releases

        Args:
            force (bool): Re-Download locally available data (Default: False)
        """

        for name, module in self._data_modules.items():
            print(f'Downloading data for {name}')
            module.download_module_data(force=force)

    def delete_module_data(self):
        """Delete any data for all combined surveys / data releases"""

        for module in self._data_modules.keys():
            module.delete_module_data()

    def get_available_ids(self):
        """Return a table of object ids available in the combined data set"""

        data_order = ['obj_id', 'release', 'survey']
        return sorted(
            zip(*[self._obj_ids[c].values.tolist() for c in data_order])
        )

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
        duplicate_data = self._obj_ids[indices]
        return sorted(duplicate_data.itertuples(index=False, name=None))

    def register_filters(self, force=False):
        """Register filters for the combined data with SNCosmo

        Args:
            force (bool): Whether to re-register a band if already registered (Default: False)
        """

        for module in self._data_modules.values():
            try:
                module.register_filters(force=force)

            except utils.NoDownloadedData:
                raise utils.NoDownloadedData(
                    f'No data downloaded for {module.__name__}')

    def get_data_for_id(self, obj_id, format_sncosmo=False):
        """Return data for a given object id

        See ``get_available_ids()`` for a table of available id values. Object

        Args:
            obj_id   (Tuple[str]): The ID of the desired object
            format_sncosmo (bool): Format data for SNCosmo.fit_lc (Default: False)

        Returns:
            An astropy table of data for the given ID
        """

        id_data = self._obj_ids[
            (self._obj_ids['obj_id'] == obj_id[0]) &
            (self._obj_ids['release'] == obj_id[1]) &
            (self._obj_ids['survey'] == obj_id[2])
        ]

        if len(id_data) == 0:
            raise ValueError('Unrecognized object ID')

        module_key = f"{id_data['survey'].iloc[0]}:{id_data['release'].iloc[0]}"
        data_module = self._data_modules[module_key]
        return data_module.get_data_for_id(
            obj_id[0], format_sncosmo=format_sncosmo)

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

        if filter_func is None:
            filter_func = lambda x: x

        id_data = self._obj_ids
        if survey is not None:
            id_data = id_data[id_data['survey'] == survey]

        if release is not None:
            id_data = id_data[id_data['release'] == release]

        for index, row in utils.build_pbar(id_data.iterrows(), verbose):
            obj_id = (row['obj_id'], row['release'], row['survey'])
            data = self.get_data_for_id(obj_id, format_sncosmo=format_sncosmo)
            if filter_func(data):
                yield data

    def get_joined_ids(self):
        pass

    def join_ids(self, *obj_ids):
        pass

    def seperate_ids(self, mapping):
        pass
