# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""The ``osc`` module provides access to supernova data hosted by the Open
Supernova Catalog. Photometric and spectroscopic data can be accessed
separately via the `OSCPhot` and `OSCSpec` classes respectively.
"""

from pathlib import Path
from typing import List

import pandas as pd
from astropy.table import Table

from sndata import utils
from sndata.base_classes import PhotometricRelease


# def query_osc_spectra(uia_name: str) -> Table:
#     """Return photometric data from the Open Supernova Catalog
#
#     Args:
#         uia_name: SN name (e.g. 'SN2011fe')
#
#     Returns:
#         A list of spectral data as dictionaries
#     """
#
#     return _query_osc(uia_name, 'spectra')


class OSCPhot(PhotometricRelease):
    """

    Deviations from the standard UI:
        - None  # Todo

    Cuts on returned data:
        - None   # Todo
    """

    survey_name = 'Open Supernova Catalog'
    survey_abbrev = 'OSC'
    release = 'OSCPhot'
    survey_url = 'https://sne.space/'
    publications = ('Guillochon et al. 2017',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2017ApJ...835...64G/abstract'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()
        self._phot_dir = self._data_dir / 'cached_photometry'

    def _get_available_tables(self) -> List[int]:
        """Get Ids for available vizier tables published by this data release"""

        return []

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        # Returned object Ids should be sorted and unique.
        # For example:
        files = self._spectra_dir.glob('*.dat')
        return sorted(set(Path(f).name for f in files))

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        osc_response = utils.query_osc(obj_id)
        data = Table.from_pandas(pd.DataFrame(osc_response))
        data.meta = osc_response

        # Todo: table formatting

        return data

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        raise NotImplementedError(
            'Data from the OSC is downloaded from the OSC database and cached '
            'to disk as needed. Downloading the entire OSC at once via the '
            '`download_module_data` function is not supported.'
        )
