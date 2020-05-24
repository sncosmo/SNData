# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""The ``osc`` module provides access to supernova data hosted by the Open
Supernova Catalog. Photometric and spectroscopic data can be accessed
separately via the `OSCPhot` and `OSCSpec` classes respectively.
"""

import json
from typing import List

import numpy as np
import requests
from astropy.table import Table, vstack

from sndata import utils
from sndata.base_classes import SpectroscopicRelease, VizierTableId


def query_osc(object: str, quantity: str = None, attribute: str = None, **kwargs):
    """Query the open supernova catalog

    Full documentation of the OSC REST API is available at
    https://github.com/astrocatalogs/OACAPI

    Args:
        object: Object(s) to query data for
        quantity: Quantity to query for object
        attribute: Sub set of quantity to return data for
        kwargs: Any arguments for sub-selecting the query

    Returns:
        Query response as a dictionary
    """

    # Construct a base query for the specified object that we can build off of as
    # https://api.sne.space/OBJECT/QUANTITY/ATTRIBUTE?ARGUMENT1=VALUE1&...
    url = f'https://api.astrocats.space/{object}/'

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

    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.content.decode('utf-8'))


class OSCBase:
    """Base class for accessing the Open Supernova Catalog"""

    survey_name = 'Open Supernova Catalog'
    survey_abbrev = 'OSC'
    release = 'OSCPhot'
    survey_url = 'https://sne.space/'
    publications = ('Guillochon et al. 2017',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2017ApJ...835...64G/abstract'

    def _get_available_tables(self) -> List[VizierTableId]:
        """Get Ids for available vizier tables published by this data release"""

        return ['catalog']

    def _load_table(self, table_id: VizierTableId, use_cached: bool = True) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
            use_cached: Whether to use results that have been cached to disk
        """

        meta_path = self._data_dir / 'catalog.json'
        with meta_path.open() as infile:
            return Table(json.load(infile))

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        meta_path = self._data_dir / 'catalog.json'
        if not meta_path.exists():
            # Download data and write to file
            osc_response = query_osc('catalog', format='csv')
            with meta_path.open() as ofile:
                json.dump(osc_response['catalog'], ofile)


class OSCSpec(SpectroscopicRelease, OSCBase):
    """

    Deviations from the standard UI:
        - None  # Todo

    Cuts on returned data:
        - None
    """

    def __init__(self):
        """Define local and remote paths of data"""

        self._data_dir = utils.find_data_dir('osc', 'spectroscopic')
        self._spectra_dir = self._data_dir / 'spectra'
        self._spectra_dir.mkdir(exist_ok=True, parents=True)

    def _get_available_ids(self, use_cached: bool = True) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        obj_id_path = self._data_dir / 'obj_id.dat'
        if use_cached and obj_id_path.exists():
            obj_ids = np.load(obj_id_path).tolist()

        else:
            obj_ids = sorted(query_osc('catalog', 'name').keys())
            np.save(obj_id_path, obj_ids)

        return obj_ids

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
            osc_response = query_osc('2011fe', 'spectra')

            spectrum_tables = []
            for spectrum_dict in osc_response['2011fe']['spectra']:
                spec_data = spectrum_dict.pop('data')
                if len(spec_data[0]) == 2:
                    names = ['wavelength', 'flux']

                else:
                    names = ['wavelength', 'flux', 'fluxerr']

                spectrum_tables.append(Table(rows=spec_data, names=names))

            out_table = vstack(spectrum_tables)
            out_table.meta = query_osc(obj_id)  # Todo: use meta data from disk
            out_table.write(local_path)  # Todo add other data from osc_response

        return out_table


class OSCPhot(OSCBase):
    """

    Deviations from the standard UI:
        - None  # Todo

    Cuts on returned data:
        - None
    """

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()
        self._phot_dir = self._data_dir / 'cached_photometry'

    @utils.lru_copy_cache()
    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        return []  # Todo

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
            data.meta = query_osc(obj_id)  # Todo: use meta data from disk
            data.write(local_path)

        return data
