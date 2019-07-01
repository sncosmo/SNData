#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

"""This module handles combining data from different data sets."""

import pandas as pd
from astropy.table import Table


class Combined_Dataset:

    def __init__(self, *data_sets):
        """Combine data from different surveys into a single data set"""

        # Create a dataframe
        self._obj_id_df = None
        for data_module in data_sets:
            _, survey, release = data_module.__name__.split('.')
            id_df = pd.DataFrame({'obj_id': data_module.get_available_ids()})
            id_df.insert(0, 'release', release)
            id_df.insert(0, 'survey', survey)

            if self._obj_id_df is None:
                self._obj_id_df = id_df

            else:
                self._obj_id_df.append(id_df, ignore_index=True)

    def get_available_ids(self):
        """Return a table of object ids available in the combined data set"""

        return Table(self._obj_id_df)

    def get_duplicate_ids(self, ignore_survey=False, ignore_release=False):
        """Return a table of duplicate object ids for the combined data set

        Args:
            ignore_survey  (bool): Don't report ids from different surveys (Default: False)
            ignore_release (bool): Don't report ids from different releases (Default: False)

        Returns:
            An astropy table of duplicate id values
        """

        pass

    def register_filters(self, force=False):
        """Register filters for the combined data with SNCosmo

        Args:
            force (bool): Whether to re-register a band if already registered (Default: False)
        """

        pass

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
