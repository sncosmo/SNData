#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the SDSS Sako18 API for spectroscopic data"""

import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Union
from urllib.parse import urljoin

from astropy.table import Column, Table, vstack

from .. import utils
from ..base_classes import SpectroscopicRelease


class Sako18Spec(SpectroscopicRelease):
    """The ``Sako18Spec`` class provides access to the **spectroscopic** data
    release of the Sloan Digital Sky Survey-II (SDSS-II) Supernova Survey
    conducted between 2005 and 2007. Light curves are presented for 10,258
    variable and transient sources discovered through repeat ugriz imaging of
    SDSS Stripe 82, a 300 deg2 area along the celestial equator. This data
    release is comprised of all transient sources brighter than r ≃ 22.5 mag
    with no history of variability prior to 2004. (Source: Sako et al. 2018)

    For the photometric data of this data release see the ``sako18`` module.

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - A spectrum is included in the data release for object ``15301``, but
          no information about this spectra is provided in the spectra summary
          table (Table 9). This spectrum is ignored.
        - Seven spectroscopically observed objects are missing a reported Ra,
          Dec, and redshift. These include: ``13046``, ``13346``, ``15833``,
          ``17134``, ``17135``, ``19819``, and ``6471``.
    """

    # General metadata
    survey_name = 'Sloan Digital Sky Survey'
    survey_abbrev = 'SDSS'
    release = 'Sako18Spec'
    survey_url = 'https://portal.nersc.gov/project/dessn/SDSS/dataRelease/'
    publications = ('Sako et al. (2018)',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2018PASP..130f4002S/abstract'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()

        # Local paths
        self._table_dir = self._data_dir / 'tables/'  # Tables from the published paper
        self._spectra_dir = self._data_dir / 'Spectra_txt'  # spectra files
        self._spectra_zip = Path(__file__).parent / 'Spectra_txt.zip'  # compressed spectra files
        self._table_names = 'master_data.txt', 'Table2.txt', 'Table9.txt', 'Table11.txt', 'Table12.txt'

        # Define urls and file names for remote data
        self._base_url = 'https://portal.nersc.gov/project/dessn/SDSS/dataRelease/'
        self._spectra_url = urljoin(self._base_url, 'Spectra.tar.gz')

    def _get_available_tables(self) -> List[str]:
        """Get Ids for available vizier tables published by this data release"""

        table_names = []
        for f in self._table_dir.glob('*.txt'):
            table_num = f.stem.strip('Table_data')
            if table_num.isnumeric():
                table_num = int(table_num)

            table_names.append(table_num)

        return sorted(table_names, key=lambda x: 0 if x == 'master' else x)

    def _load_table(self, table_id: Union[int, str]) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        if table_id not in self.get_available_tables():
            raise ValueError(f'Table {table_id} is not available.')

        if table_id == 'master':
            table = Table.read(self._table_dir / 'master_data.txt', format='ascii')

        else:
            table = Table.read(
                self._table_dir / f'Table{table_id}.txt', format='ascii')

        table['CID'] = Column(table['CID'], dtype=str)
        if table_id == 9:
            table['SID'] = Column(table['SID'], dtype=str)

        return table

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        return sorted(set(self.load_table(9)['CID']))

    # noinspection PyUnusedLocal
    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        # Read in all spectra for the given object Id
        data_tables = []
        files = list(self._spectra_dir.glob(f'sn{obj_id}-*.txt'))
        files += list(self._spectra_dir.glob(f'gal{obj_id}-*.txt'))
        for path in files:
            data = Table.read(path, format='ascii', names=['wavelength', 'flux'])
            extraction_type = path.stem.split('-')[0].strip(obj_id)
            spec_id = path.stem.split('-')[-1]

            # Get type of object observed by spectra
            spectra_summary = self.load_table(9)
            summary_row = spectra_summary[spectra_summary['SID'] == spec_id][0]
            spec_type = 'Gal' if extraction_type == 'gal' else summary_row['Type']

            # Get meta data for the current spectrum from the summary table
            data['sid'] = spec_id
            data['type'] = spec_type
            data['telescope'] = summary_row['Telescope']

            # Determine observed date in JD
            observed_date = summary_row['Date']
            if format_table:
                date_with_timezone = summary_row['Date'] + '+0000'
                date = datetime.strptime(date_with_timezone, '%Y-%m-%d%z')

                unix_time = date.timestamp()
                january_1_1970_in_julian = 2440587.5
                day_in_seconds = 24 * 60 * 60
                data['time'] = (unix_time / day_in_seconds) + january_1_1970_in_julian

            else:
                data['date'] = observed_date

            data_tables.append(data)

        out_data = vstack(data_tables)
        out_data.meta['obj_id'] = obj_id

        # Add meta data from the master table
        master_table = self.load_table('master')
        phot_record = master_table[master_table['CID'] == obj_id]

        if phot_record:
            out_data.meta['ra'] = phot_record['RA'][0]
            out_data.meta['dec'] = phot_record['DEC'][0]
            out_data.meta['z'] = phot_record['zCMB'][0]
            out_data.meta['z_err'] = phot_record['zerrCMB'][0]

        else:
            # Known cases include the following object ids:
            # '13046', '13346', '15833', '17134', '17135', '19819', '6471'
            out_data.meta['ra'] = None
            out_data.meta['dec'] = None
            out_data.meta['z'] = None
            out_data.meta['z_err'] = None

        out_data.meta['dtype'] = 'spectroscopic'
        return out_data

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        for file_name in self._table_names:
            utils.download_file(
                url=self._base_url + file_name,
                path=self._table_dir / file_name,
                force=force,
                timeout=timeout
            )

        # Spectral data parsing requires IRAF so we use preparsed data instead
        if force or not self._spectra_dir.exists():
            with zipfile.ZipFile(self._spectra_zip, 'r') as zip_ref:
                zip_ref.extractall(self._data_dir)
