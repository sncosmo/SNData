#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module handles combining data from different data sets."""

import logging
from copy import copy
from typing import List, Tuple, Union

import pandas as pd
from astropy.table import Table, vstack

from . import _utils as utils
from . import csp, des, essence, jla, sdss
from .exceptions import InvalidObjId, ObservedDataTypeError

CombinedID = Tuple[str]
log = logging.getLogger(__name__)


# Todo: Test this function with a dedicated unit test
def get_zp(band_name: str) -> float:
    """Return the zero point used by sndata for a given bandpass

    bandpass names are case sensitive.

    Args:
        band_name: The name of the sndata bandpass

    Returns:
        The zero point as a float
    """

    survey, release, *_ = band_name.split('_')
    modules_dict = {
        'dr1': csp.DR1,
        'dr3': csp.DR3,
        'sn3yr': des.SN3YR,
        'narayan16': essence.Narayan16,
        'betoule14': jla.Betoule14,
        'sako18': sdss.Sako18
    }

    data_class = modules_dict[release]
    if not hasattr(data_class, 'band_names'):
        raise ObservedDataTypeError(
            'Survey {} {} does not have registered photometric band passes.')

    return data_class.get_zp_for_band(band_name)


def _reduce_id_mapping(id_list: List[CombinedID]) -> list:
    """Combine a list of sets by combining any sets with shared elements

    Args
        id_list: List of object IDs to join

    Returns:
        A list of combined sets
    """

    old_id_list = copy(id_list)
    new_id_list = []

    while old_id_list:
        first, *rest = old_id_list

        lf = -1
        while len(first) > lf:
            lf = len(first)
            rest2 = []
            for r in rest:
                if len(first.intersection(r)) > 0:
                    first |= r

                else:
                    rest2.append(r)

            rest = rest2

        if len(first) > 1:
            new_id_list.append(first)

        old_id_list = rest

    return new_id_list


class CombinedDataset:
    """Combine data from different surveys into a single data set

    Args:
        data_sets (iter[module]): SNData module for a specific data release
    """

    def __init__(self, *data_sets):

        # Enforce same metadata attributes as a single data release
        self.survey_name = tuple(ds.survey_name for ds in data_sets)
        self.survey_abbrev = tuple(ds.survey_abbrev for ds in data_sets)
        self.release = tuple(ds.release for ds in data_sets)
        self.survey_url = tuple(ds.survey_url for ds in data_sets)
        self.data_type = tuple(ds.data_type for ds in data_sets)
        self.publications = tuple(ds.publications for ds in data_sets)
        self.ads_url = tuple(ds.ads_url for ds in data_sets)

        # Store data access classes for each data release
        self._data_releases = dict()
        for module in set(data_sets):
            module_id = f'{module.survey_abbrev}:{module.release}'
            self._data_releases[module_id] = module

        self._joined_ids = []

        # To store combined table of all object ids
        # We don't load the table at init in case some data isn't downloaded
        self._obj_id_dataframe = None

    @property
    def _obj_ids(self) -> pd.DataFrame:
        if self._obj_id_dataframe is not None:
            return self._obj_id_dataframe

        # Create a DataFrame of combined object IDs
        obj_id_dataframe = None
        for data_module in self._data_releases.values():
            id_df = pd.DataFrame({'obj_id': data_module.get_available_ids()})
            id_df.insert(0, 'release', data_module.release)
            id_df.insert(0, 'survey', data_module.survey_abbrev)

            if obj_id_dataframe is None:
                obj_id_dataframe = id_df

            else:
                obj_id_dataframe = obj_id_dataframe.append(
                    id_df, ignore_index=True)

        self._obj_id_dataframe = obj_id_dataframe
        return self._obj_id_dataframe

    @property
    def band_names(self) -> Tuple[str]:
        """Assuming all the combined data releases are photometric
        return the unique bandpass names
        """

        # This will raise an error if any data releases are spectroscopic
        # That is OK!
        all_band_names = set()
        for release in self._data_releases.values():
            all_band_names.update(release.band_names)

        return tuple(sorted(all_band_names))

    @property
    def zero_point(self) -> Tuple[float]:
        return tuple(get_zp(b) for b in self.band_names)

    def download_module_data(self, force: bool = False):
        """Download data for all combined surveys / data releases

        Args:
            force: Re-Download locally available data (Default: False)
        """

        for name, module in self._data_releases.items():
            log.info(f'Downloading data for {name}')
            module.download_module_data(force=force)

    def delete_module_data(self):
        """Delete any data for all combined surveys / data releases"""

        for module in self._data_releases.values():
            module.delete_module_data()

    def get_available_ids(self) -> List[CombinedID]:
        """Return a table of object IDs available in the combined data set"""

        data_order = ['obj_id', 'release', 'survey']
        return sorted(
            zip(*[self._obj_ids[c].values.tolist() for c in data_order])
        )

    def register_filters(self, force: bool = False):
        """Register filters for the combined data with SNCosmo

        Args:
            force: Re-register a band if already registered (Default: False)
        """

        for data_class in self._data_releases.values():
            try:
                data_class.register_filters(force=force)

            except utils.NoDownloadedData:
                raise utils.NoDownloadedData(
                    f'No data downloaded for {data_class.__name__}')

    def _get_data_single_id(
            self, obj_id: Tuple[str], format_table: bool = True) -> Table:
        """Return data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format data for SNCosmo.fit_lc (Default: False)

        Returns:
            An astropy table of data for the given ID
        """

        id_data = self._obj_ids[
            (self._obj_ids['obj_id'] == obj_id[0]) &
            (self._obj_ids['release'] == obj_id[1]) &
            (self._obj_ids['survey'] == obj_id[2])
            ]

        if len(id_data) == 0:
            raise InvalidObjId(f'Unrecognized object ID: {obj_id}')

        module_key = f"{id_data['survey'].iloc[0]}:{id_data['release'].iloc[0]}"
        data_module = self._data_releases[module_key]
        return data_module.get_data_for_id(obj_id[0], format_table=format_table)

    def _get_data_id_list(
            self, obj_id_list: List[CombinedID], format_table: bool = True):
        """Return data for a list of object ID

        Data tables for individual object IDs are vertically stacked. Meta
        data for each individual obj_id is stored in the combined

        Args:
            obj_id_list: The ID of the desired object
            format_table: Format data for SNCosmo.fit_lc (Default: False)

        Returns:
            An astropy table of data for the given ID
        """

        first_id = obj_id_list.pop()
        combined_table = self._get_data_single_id(first_id, format_table)
        combined_table.meta = {
            first_id: combined_table.meta,
            'obj_id': [first_id]
        }

        del combined_table.meta[first_id]['obj_id']

        for obj_id in obj_id_list:
            data_table = self._get_data_single_id(obj_id, format_table)

            new_meta = data_table.meta
            data_table.meta = {}
            del new_meta['obj_id']

            combined_table = vstack((combined_table, data_table))
            combined_table.meta['obj_id'].append(obj_id)
            combined_table.meta[obj_id] = new_meta

        return combined_table

    def get_data_for_id(
            self, obj_id: CombinedID, format_table: bool = True) -> Table:
        """Return data for a given object ID

        See ``get_available_ids()`` for a table of available ID values. Object

        Args:
            obj_id   (tuple[str]): The ID of the desired object
            format_table   (bool): Format data for SNCosmo.fit_lc (Default: False)

        Returns:
            An astropy table of data for the given ID
        """

        for id_set in self._joined_ids:
            if obj_id in id_set:
                return self._get_data_id_list(id_set, format_table)

        return self._get_data_single_id(obj_id, format_table)

    def iter_data(
            self,
            survey: str = None,
            release: str = None,
            verbose: Union[bool, dict] = False,
            format_table: bool = True,
            filter_func: callable = None) -> Table:
        """Iterate through all available targets and yield data tables

        An optional progress bar can be formatted by passing a dictionary of tqdm
        arguments. Outputs can be optionally filtered by passing a function
        ``filter_func`` that accepts a data table and returns a boolean.

        Args:
            survey: Only include data from a given survey (Default: None)
            release: Only include data from a given data release (Default: None)
            verbose: Optionally display progress bar while iterating (Default: False)
            format_table: Format data for SNCosmo.fit_lc (Default: False)
            filter_func: An optional function to filter outputs by

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
            data = self.get_data_for_id(obj_id, format_table=format_table)
            if filter_func(data):
                yield data

    def get_joined_ids(self) -> List[CombinedID]:
        """Return a list of joined object IDs

        Return:
            A list of joined object IDs [{id_1, id_2}, ...]
        """

        return copy(self._joined_ids)

    def join_ids(self, *obj_ids: CombinedID):
        """Join object ID values to indicate the same object

        Args:
            obj_ids: Object IDs to join
        """

        if len(obj_ids) <= 1:
            raise ValueError(
                'Object IDs can only be joined in sets of 2 or more.')

        self._joined_ids.append(set(obj_ids))
        self._joined_ids = _reduce_id_mapping(self._joined_ids)

    def separate_ids(self, *obj_ids: CombinedID):
        """Separate object IDs so they are no longer joined to other IDs

        Args:
            obj_ids: List of object IDs to separate
        """

        if len(obj_ids) <= 1:
            raise ValueError(
                'Object IDs can only be separated in sets of 2 or more.')

        obj_ids = set(obj_ids)
        for obj_id_set in self._joined_ids:
            obj_id_set -= obj_ids

        self._joined_ids = _reduce_id_mapping(self._joined_ids)
