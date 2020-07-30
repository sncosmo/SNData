#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the BSNIP Stahl20 API"""

from astropy.table import Table
from typing import List

from .. import utils
from ..base_classes import SpectroscopicRelease

_table_url_data = {
    1: 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPI/obj_info_table.txt',
    2: 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPI/spec_info_table.txt',
    5: 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPI/SNID_templates_table.txt',
    7: 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPI/snid_info_table.txt',
    3: 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/ben_vel.txt',
    'A1': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/data_summary.txt',
    'B1': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/cahk.txt',
    'B2': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/si4000.txt',
    'B3': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/mg.txt',
    'B4': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/fe.txt',
    'B5': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/sii.txt',
    'B6': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/si5972.txt',
    'B7': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/si6355.txt',
    'B8': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/oi.txt',
    'B9': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/cair.txt'

}


class Silverman12(SpectroscopicRelease):
    """The first data release of the the Berkeley Supernova Ia Program
    (BSNIP), including 1298 low-redshift (z ≲ 0.2) optical spectra of 582 Type
    Ia supernovae (SNe Ia) observed from 1989 to 2008. Most of the data were
    obtained using the Kast double spectrograph mounted on the Shane 3 m
    telescope at Lick Observatory and have a typical wavelength range of
    3300-10 400 Å. (Source:  Stahl et al. 2012)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    survey_name = 'Berkeley Supernova Ia Program'
    survey_abbrev = 'BSNIP'
    release = 'Silverman12'
    survey_url = 'http://heracles.astro.berkeley.edu/sndb/'
    publications = ('Silverman et al. 2012a', 'Silverman et al. 2012b')
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2012MNRAS.425.1789S/abstract'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()
        self._spectra_dir = self._data_dir / 'spectra'
        self._table_dir = self._data_dir / 'tables'

        self._spectra_url = 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPI/BSNIPI_spectra.tar.gz'

    def _get_available_tables(self) -> List[str]:
        """Get Ids for available vizier tables published by this data release"""

        return sorted(_table_url_data.keys(), key=str)

    def _load_table(self, table_id: str) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        raise NotImplementedError

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        raise NotImplementedError

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        raise NotImplementedError

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        try:
            utils.download_tar(
                url=self._spectra_url,
                out_dir=self._spectra_dir,
                skip_exists=self._spectra_dir,
                mode='r:gz',
                force=force,
                timeout=timeout
            )

        except EOFError:  # Official file is not formatted correctly?
            pass

        for table_id, url in _table_url_data.items():
            utils.download_file(
                url=url,
                destination=self._table_dir / f'table{table_id}.dat',
                force=force,
                timeout=timeout
            )
