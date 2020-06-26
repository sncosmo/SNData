#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the BSNIP Stahl20 API"""

from typing import List

from astropy.io.ascii.core import InconsistentTableError
from astropy.table import Table, vstack

from .. import utils
from ..base_classes import SpectroscopicRelease


class Stahl20(SpectroscopicRelease):
    """The second data release of the the Berkeley Supernova Ia Program
    (BSNIP), including 637 low-redshift optical spectra collected  between
    2009 and 2018. Targets include 626 spectra (of 242 objects) that are
    unambiguously classified as belonging to Type Ia supernovae (SNe Ia).
    Of these, 70 spectra of 30 objects are classified as spectroscopically
    peculiar and 79 SNe Ia (covered by 328 spectra) have complementary
    photometric coverage. The median SN in the data set has one epoch of
    spectroscopy, a redshift of 0.0208 (with a low of 0.0007 and high of
    0.1921), and is first observed spectroscopically 1.1 days after maximum
    light. (Source:  Stahl et al. 2020)

    Deviations from the standard UI:
        - Meta data such as object Ra, DEC, and redshifts ar not included
          in the official data release files.

    Cuts on returned data:
        - None
    """

    survey_name = 'Berkeley Supernova Ia Program'
    survey_abbrev = 'BSNIP'
    release = 'Stahl20'
    survey_url = 'http://heracles.astro.berkeley.edu/sndb/'
    publications = ('Stahl et al. 2020',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2020MNRAS.492.4325S/abstract'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()
        self._spectra_dir = self._data_dir / 'spectra'
        self._table_dir = self._data_dir / 'tables'
        self._meta_data_path = self._data_dir / 'meta_data.yml'

        # Define urls / path for remote / local data.
        self._spectra_url = 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPdata2/spectra.tar.gz'
        self._meta_table_url = 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPdata2/spectra.csv'
        self._meta_table_path = self._table_dir / 'meta_data.csv'

    def _get_available_tables(self) -> List[str]:
        """Get Ids for available vizier tables published by this data release"""

        if self._meta_table_path.exists():
            return ['meta_data']

        return []

    def _load_table(self, table_id: str) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        return Table.read(self._table_dir / (table_id + '.csv'))

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        obj_ids = self.load_table('meta_data')['ObjName']
        return sorted(set(obj_ids))

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        data_tables = []
        meta_data = self.load_table('meta_data')
        object_meta = meta_data[meta_data['ObjName'] == obj_id]
        for row in object_meta:
            path = self._spectra_dir / row['Filename']

            # Tables either have two or three columns
            try:
                table = Table.read(
                    path, format='ascii',
                    names=['wavelength', 'flux', 'fluxerr'])

            except InconsistentTableError:
                table = Table.read(
                    path, format='ascii',
                    names=['wavelength', 'flux'])

            if format_table:
                table['time'] = utils.convert_ut_to_jd(row['UT_Date'])
                table['instrument'] = row['Instrument']

            data_tables.append(table)

        all_data = vstack(data_tables)
        all_data.sort('wavelength')
        all_data.meta['obj_id'] = obj_id
        all_data.meta['ra'] = None
        all_data.meta['dec'] = None
        all_data.meta['z'] = None
        all_data.meta['z_err'] = None

        # Return data with columns in a standard order
        return all_data

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        utils.download_file(
            url=self._meta_table_url,
            path=self._meta_table_path,
            force=force,
            timeout=timeout
        )

        utils.download_tar(
            url=self._spectra_url,
            out_dir=self._data_dir,
            skip_exists=self._spectra_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )
