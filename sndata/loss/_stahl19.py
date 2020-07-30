#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the LOSS Stahl19 API"""

from typing import List

import numpy as np
from astropy.table import Table

from .. import utils
from ..base_classes import DefaultParser, PhotometricRelease


# Todo: Add zero points and convert magnitudes to fluxes in formatted table
class Stahl19(PhotometricRelease, DefaultParser):
    """The ``Stahl19`` class provides access to 93 Type Ia supernovae (SNe Ia)
    from the second data release of the Lick Observatory Supernova Search
    (LOSS) conducted between 2005 and 2018. It consists of 78 spectroscopically
    normal SNe Ia, with the remainder divided between distinct subclasses
    (3 SN 1991bg-like, 3 SN 1991T-like, 4 SNe Iax, 2 peculiar, and 3
    super-Chandrasekhar events), and has a median redshift of 0.0192.
    The sample has a median coverage of 16 photometric epochs at a cadence
    of 5.4 d, and the median first observed epoch is ∼4.6 d before
    maximum B-band light.  (Source: Stahl et al. 2019)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    survey_name = 'Lick Observatory Supernova Search'
    survey_abbrev = 'LOSS'
    release = 'Stahl19'
    survey_url = 'None'
    data_type = 'photometric'
    publications = ('Stahl et al. (2019)',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2019MNRAS.490.3882S/abstract'

    band_names = (
        'loss_stahl19_B_kait3',
        'loss_stahl19_B_kait4',
        'loss_stahl19_B_nickel1',
        'loss_stahl19_B_nickel2',
        'loss_stahl19_I_kait3',
        'loss_stahl19_I_kait4',
        'loss_stahl19_I_nickel1',
        'loss_stahl19_I_nickel2',
        'loss_stahl19_R_kait3',
        'loss_stahl19_R_kait4',
        'loss_stahl19_R_nickel1',
        'loss_stahl19_R_nickel2',
        'loss_stahl19_V_kait3',
        'loss_stahl19_V_kait4',
        'loss_stahl19_V_nickel1',
        'loss_stahl19_V_nickel2')

    # Taken from Ganeshalingam et al. 2013
    # https://ui.adsabs.harvard.edu/abs/2013MNRAS.433.2240G/abstract
    zero_point = [
        15.332,
        15.249,
        15.224,
        np.nan,
        14.457,
        14.439,
        14.703,
        np.nan,
        15.008,
        14.973,
        14.930,
        np.nan,
        14.921,
        14.922,
        14.828,
        np.nan
    ]

    def __init__(self):
        """Define local and remote paths of data"""

        # Call to parent class defines the self._data_dir attribute
        # All data should be downloaded to / read from that directory
        super().__init__()

        # Define data urls
        self._table_2_url = 'http://heracles.astro.berkeley.edu/sndb/static/LOSS2/Table2.txt'
        self._table_b3_url = 'http://heracles.astro.berkeley.edu/sndb/static/LOSS2/TableB3.txt'
        self._filter_url = 'http://heracles.astro.berkeley.edu/sndb/static/LOSS2/transmission_curves.tar.gz'

        # Local data paths
        self._table_2_path = self._table_dir / 'Table2.txt'
        self._table_b3_path = self._table_dir / 'TableB3.txt'
        self._filter_dir = self._data_dir / 'transmission_curves'
        self._filter_file_names = (
            'B_kait3.txt',
            'B_kait4.txt',
            'B_nickel1.txt',
            'B_nickel2.txt',
            'I_kait3.txt',
            'I_kait4.txt',
            'I_nickel1.txt',
            'I_nickel2.txt',
            'R_kait3.txt',
            'R_kait4.txt',
            'R_nickel1.txt',
            'R_nickel2.txt',
            'V_kait3.txt',
            'V_kait4.txt',
            'V_nickel1.txt',
            'V_nickel2.txt')

    def _get_available_tables(self) -> List[int]:
        """Get Ids for available vizier tables published by this data release"""

        table_nums = []
        for f in self._table_dir.rglob('Table*.txt'):
            table_number = f.stem.lstrip('Table')
            try:
                table_number = int(table_number)

            # Table from appendix and has letter in name. E.g. 'B3'
            except ValueError:
                pass

            table_nums.append(table_number)

        return table_nums

    def _load_table(self, table_id: int) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        table_path = self._table_dir / f'Table{table_id}.txt'
        table = Table.read(table_path, format='ascii')
        table = Table(table, masked=True)  # Convert to a masked table
        for col in table.columns.values():
            col.mask = col == 99.999

        return table

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        return sorted(np.unique(self.load_table(2)['SN']))

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        # Unformatted table has a separate column for each bandpass
        table_2 = self.load_table(2)
        object_data = table_2[table_2['SN'] == obj_id]

        if format_table:
            formatted_rows = []
            for row in object_data:
                for band in 'BVRI':
                    band_name = f'loss_stahl19_{band}_{row["system"]}'
                    zp = self.zero_point[self.band_names.index(band_name)]
                    formatted_rows.append(
                        [row['MJD'], band_name, zp, 'Landolt',
                         row[band], row['E' + band]]
                    )

            object_data = Table(
                rows=formatted_rows,
                names=['time', 'band', 'zp', 'zpsys', 'mag', 'magerr'])

            object_data['time'] = utils.convert_to_jd(object_data['time'], 'mjd')
            object_data['flux'] = 10 ** ((object_data['mag'] - object_data['zp']) / -2.5)
            object_data['fluxerr'] = (np.log(10) / -2.5) * object_data['flux'] * object_data['magerr']

        object_data.meta = {
            'obj_id': obj_id,
            'ra': None,
            'dec': None,
            'z': None,
            'z_err': None,
        }

        return object_data

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        urls = (self._table_2_url, self._table_b3_url)
        paths = (self._table_2_path, self._table_b3_path)
        for file_url, file_path in zip(urls, paths):
            utils.download_file(
                url=file_url,
                destination=file_path,
                force=force,
                timeout=timeout
            )

        utils.download_tar(
            url=self._filter_url,
            out_dir=self._data_dir,
            skip_exists=self._filter_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )
