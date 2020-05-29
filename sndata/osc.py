# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""The ``osc`` module provides access to supernova data hosted by the Open
Supernova Catalog. Photometric and spectroscopic data can be accessed
separately via the `OSCPhot` and `OSCSpec` classes respectively.
"""

import json
from functools import lru_cache
from typing import List

import requests
from astropy.table import Table, vstack

from sndata import utils
from sndata.base_classes import PhotometricRelease, SpectroscopicRelease, VizierTableId
from sndata.exceptions import InvalidTableId, NoDownloadedData


def query_osc(object: str, quantity: str = None, attribute: str = None,
              timeout=None, verbose=False, **kwargs):
    """Query the open supernova catalog

    Function signature follows the the OSC REST API. Full documentation of the
    OSC API is available at https://github.com/astrocatalogs/OACAPI .

    Args:
        object: Object(s) to query data for
        quantity: Quantity to query for object
        attribute: Sub set of quantity to return data for
        timeout: Seconds before request timeout
        verbose: Print fetched URL from request
        kwargs: Any arguments for sub-selecting the query

    Returns:
        Query response as a dictionary
    """

    # Construct a base query for the specified object that we can build off of as
    # https://api.sne.space/OBJECT/QUANTITY/ATTRIBUTE?ARGUMENT1=VALUE1&...
    url = f'https://api.sne.space/{object}/'

    if quantity:
        url += f'{quantity}/'

    elif attribute:
        # Attributes are a subset of the quantity.
        raise RuntimeError('Cannot query ``attribute`` without ``quantity``')

    if attribute:
        url += f'{attribute}/'

    if kwargs:
        url += '?'
        for key, value in kwargs.items():
            url += key
            if value is not None:
                url += f'={value}'

        url += '&'

    if verbose:
        print(f'Fetching {url}')

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return json.loads(response.content.decode('utf-8'))


class OSCBase:
    """Mixin class for accessing the Open Supernova Catalog"""

    survey_name = 'Open Supernova Catalog'
    survey_abbrev = 'OSC'
    survey_url = 'https://sne.space/'
    publications = ('Guillochon et al. 2017',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2017ApJ...835...64G/abstract'

    def __init__(self):

        super().__init__()
        self._meta_path = self._data_dir / 'catalog.json'

    def get_available_tables(self) -> List[VizierTableId]:
        """Get Ids for available vizier tables published by this data release"""

        return ['catalog']

    @lru_cache(maxsize=None)  # Cache I/O result
    def _object_meta_data(self) -> dict:
        """Return object meta data as a dictionary"""

        if not self._meta_path.exists():
            raise NoDownloadedData()

        with self._meta_path.open() as infile:
            return json.load(infile)

    def load_table(self, table_id: VizierTableId) -> Table:
        """Return a table published by this data release

        Args:
            table_id: The published table number or table name
        """
        if table_id == 'catalog':
            return self._object_meta_data()  # Todo: Return a table instead of a dictionary

        raise InvalidTableId()

    def download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        if force or not self._meta_path.exists():
            osc_response = query_osc('catalog', timeout=timeout, verbose=True)

            self._meta_path.parent.mkdir(parents=True, exist_ok=True)
            with self._meta_path.open('w') as ofile:
                json.dump(osc_response, ofile)


class OSCSpec(OSCBase, SpectroscopicRelease):
    """

    Deviations from the standard UI:
        - None  # Todo

    Cuts on returned data:
        - None
    """

    release = 'OSCSpec'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()
        self._spectra_dir = self._data_dir / 'spectra'
        self._spectra_dir.mkdir(exist_ok=True, parents=True)

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        # Todo: Some of these objects may not have spectroscopic data
        return sorted(self._object_meta_data().keys())

    @staticmethod
    def _osc_spec_to_table(spectrum_dict: dict) -> Table:
        """Typecast an OSC spectrum from a dictionary to a Table

        Args:
            spectrum_dict: The OSC spectrum

        Returns:
            An astropy table
        """

        spec_data = spectrum_dict.pop('data')
        if len(spec_data[0]) == 2:
            names = ['wavelength', 'flux']
            dtype = [float, float]

        else:
            names = ['wavelength', 'flux', 'fluxerr']
            dtype = [float, float, float]

        spec_table = Table(rows=spec_data, names=names, dtype=dtype)
        for k, v in spectrum_dict.items():
            spec_table[k] = v

        return spec_table

    def _get_data_for_id(self, obj_id: str, use_cached: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            use_cached: Whether to use results that have been cached to disk

        Returns:
            An astropy table of data for the given ID
        """

        local_path = self._spectra_dir / f'{obj_id.lower()}.ecsv'
        if use_cached and local_path.exists():
            out_table = Table.read(local_path)

        else:
            osc_spectra = query_osc(obj_id, 'spectra')[obj_id]['spectra']
            out_table = vstack([self._osc_spec_to_table(sdict) for sdict in osc_spectra])

            # Todo: Format meta data to meet package standards
            out_table.meta = {'obj_id': obj_id}
            out_table.meta.update(self._object_meta_data()[obj_id])
            out_table.write(local_path)

        return out_table


class OSCPhot(OSCBase, PhotometricRelease):
    """

    Deviations from the standard UI:
        - None  # Todo

    Cuts on returned data:
        - None
    """

    release = 'OSCPhot'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()
        self._phot_dir = self._data_dir / 'cached_photometry'

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        # Todo: Some of these objects may not have photometric data
        return sorted(self._object_meta_data().keys())

    def _get_data_for_id(self, obj_id: str, use_cached: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            use_cached: Whether to use results that have been cached to disk

        Returns:
            An astropy table of data for the given ID
        """

        local_path = self._phot_dir / f'{obj_id.lower()}.ecsv'
        if use_cached and local_path.exists():
            data = Table.read(local_path)

        else:
            osc_response = query_osc(obj_id, 'photometry')
            data = Table(osc_response[obj_id]['photometry'])

            # Todo: Format meta data to meet package standards
            data.meta = {'obj_id': obj_id}
            data.meta.update(self._object_meta_data()[obj_id])
            data.write(local_path)

        # Todo: format data to meet some kind of uniform standard
        return data
