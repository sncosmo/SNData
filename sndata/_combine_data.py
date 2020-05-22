#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module handles combining data from different data sets."""

from copy import copy
from functools import lru_cache
from typing import List, Tuple, Union

import pandas as pd
from astropy.table import Table, vstack

from . import csp, des, essence, jla, sdss, sweetspot
from . import utils as utils
from .exceptions import InvalidObjId, InvalidTableId, ObservedDataTypeError

CombinedID = Union[str, Tuple[str, str, str]]


# Todo: Test this function with a dedicated unit test
def get_zp(band_name: str) -> float:
    """Return the zero point used by sndata for a given bandpass

    bandpass names are case sensitive.

    Args:
        band_name: The name of the sndata bandpass

    Returns:
        The zero point as a float
    """

    modules_dict = {
        'csp_dr1': csp.DR1,
        'csp_dr3': csp.DR3,
        'des_sn3yr': des.SN3YR,
        'essence_narayan16': essence.Narayan16,
        'jla_betoule14': jla.Betoule14,
        'sdss_sako18': sdss.Sako18,
        'sweetspot_dr1': sweetspot.DR1
    }

    survey, release, *_ = band_name.split('_')
    key = f'{survey}_{release}'
    data_class = modules_dict[key]

    if not hasattr(data_class, 'band_names'):
        raise ObservedDataTypeError(
            'Survey {} {} does not have registered photometric band passes.')

    return data_class.get_zp_for_band(band_name)


def _reduce_id_mapping(id_list: List[CombinedID]) -> list:
    """Combine a list of sets by joining any sets with shared elements

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
        data_sets: SNData module for a specific data release
    """

    def __init__(self, *data_sets):

        # Enforce the same metadata attributes as a single data release
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

    @property
    @lru_cache(None)
    def _obj_id_dataframe(self):
        # Return a data frame of object Id's and their survey / release names

        return pd.DataFrame(
            self.get_available_ids(),
            columns=['obj_id', 'release', 'survey']).set_index('obj_id')

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
        """Get the zeropoint from each of the combined data releases"""

        return tuple(get_zp(b) for b in self.band_names)

    def get_available_tables(self):
        """Get Ids for vizier tables published by the combined data releases"""

        table_id_list = []
        for data_class in self._data_releases.values():
            survey_abbrev = data_class.survey_abbrev
            release = data_class.release
            for table_id in data_class.get_available_tables():
                table_id_list.append((survey_abbrev, release, table_id))

        return table_id_list

    def load_table(self, table_id):
        """Return a Vizier table published by the combined data releases

        Args:
            table_id: The published table number or table name
        """

        survey_abbrev, release, table_id = table_id
        try:
            data_class = self._data_releases[f'{survey_abbrev}:{release}']
            return data_class.load_table(table_id)

        except KeyError:
            raise InvalidTableId()

    def get_available_ids(self) -> List[CombinedID]:
        """Return a list of target object IDs for the combined data releases

        Returns:
            A list of object IDs as tuples
        """

        all_obj_ids = set()
        for data_class in self._data_releases.values():
            survey_abbrev = data_class.survey_abbrev
            release = data_class.release
            for obj_id in data_class.get_available_ids():
                all_obj_ids.add((obj_id, release, survey_abbrev))

        # Remove joined Id's
        for obj_id_set in self._joined_ids:
            obj_id_set = obj_id_set.copy()
            obj_id_set.pop()
            all_obj_ids -= obj_id_set

        return sorted(all_obj_ids)

    def _get_data_single_id(
            self, obj_id: CombinedID, format_table: bool = True) -> Table:
        """Return data for a single object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format data for SNCosmo.fit_lc

        Returns:
            An astropy table of data for the given ID
        """

        # If object_id is a tuple, get survey and release names from tuple
        if isinstance(obj_id, tuple):
            single_obj_id, release, survey_abbrev = obj_id

        # Get survey and release names from self._obj_id_dataframe
        else:
            try:
                obj_id_parent = self._obj_id_dataframe.loc[obj_id]

            except KeyError:
                raise InvalidObjId()

            if not isinstance(obj_id_parent, pd.Series):
                raise RuntimeError(f'Multiple results for obj_id: {obj_id}')

            release = obj_id_parent.release
            survey_abbrev = obj_id_parent.survey
            single_obj_id = obj_id

        data_class = self._data_releases[f"{survey_abbrev}:{release}"]
        return data_class.get_data_for_id(single_obj_id, format_table)

    def _get_data_id_list(
            self, obj_id_list: List[CombinedID], format_table: bool = True):
        """Return data for a list of object IDs

        Data tables for individual object IDs are vertically stacked. Meta
        data for each individual obj_id is stored in the combined.
        See ``get_available_ids()`` for a list of available ID values.

        Args:
            obj_id_list: The IDs of the desired objects
            format_table: Format data into the ``sndata`` standard format

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
            obj_id: The ID of the desired object
            format_table: Format data for SNCosmo.fit_lc (Default: False)

        Returns:
            An astropy table of data for the given ID
        """

        for id_set in self._joined_ids:
            if obj_id in id_set:
                return self._get_data_id_list(id_set, format_table)

        return self._get_data_single_id(obj_id, format_table)

    def iter_data(
            self,
            verbose: Union[bool, dict] = False,
            format_table: bool = True,
            filter_func: callable = None) -> Table:
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

        for obj_id in utils.build_pbar(self.get_available_ids(), verbose):
            data = self.get_data_for_id(obj_id, format_table=format_table)
            if filter_func(data):
                yield data

    def register_filters(self, force: bool = False):
        """Register filters for the combined data releases with sncosmo

        Args:
            force: Re-register a band if already registered
        """

        for data_class in self._data_releases.values():
            try:
                data_class.register_filters(force=force)

            except utils.NoDownloadedData:
                raise utils.NoDownloadedData(
                    f'No data downloaded for {data_class.__name__}')

    def download_module_data(self, force: bool = False, timeout: int = 15):
        """Download data for all combined data releases

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        for name, module in self._data_releases.items():
            module.download_module_data(force=force, timeout=timeout)

    def delete_module_data(self):
        """Delete any data for all combined surveys / data releases"""

        for module in self._data_releases.values():
            module.delete_module_data()

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

        if not all(isinstance(obj_id, tuple) for obj_id in obj_ids):
            raise TypeError('Can only join object Id\'s as tuples')

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
