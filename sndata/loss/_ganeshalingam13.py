#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the LOSS ganeshalingam13 API"""

from functools import lru_cache
from typing import List

import numpy as np
from astropy.table import Table

from .. import utils
from ..base_classes import DefaultParser, PhotometricRelease


class Ganeshalingam13(PhotometricRelease, DefaultParser):
    """The ``Ganeshalingam13`` class provides access to BVRI light curves of
    165 objects published by the first data release of the Lick Observatory
    Supernova Search (LOSS) conducted between 198 and 2008.


     It consists of 78 spectroscopically
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
    release = 'Ganeshalingam13'
    survey_url = 'None'
    data_type = 'photometric'
    publications = ('Stahl et al. (2019)',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2019MNRAS.490.3882S/abstract'

    _filter_file_names = [
        'B_kait1_shifted.txt',
        'V_kait1_shifted.txt',
        'R_kait1_shifted.txt',
        'R_kait1_shifted.txt',
        'B_kait2_shifted.txt',
        'V_kait2_shifted.txt',
        'R_kait2_shifted.txt',
        'R_kait2_shifted.txt',
        'B_kait3_shifted.txt',
        'V_kait3_shifted.txt',
        'R_kait3_shifted.txt',
        'R_kait3_shifted.txt',
        'B_kait4_shifted.txt',
        'V_kait4_shifted.txt',
        'R_kait4_shifted.txt',
        'R_kait4_shifted.txt',
        'B_nickle_shifted.txt',
        'V_nickle_shifted.txt',
        'R_nickle_shifted.txt',
        'R_nickle_shifted.txt'
    ]

    band_names = (
        'loss_ganeshalingam13_B_kait1',
        'loss_ganeshalingam13_V_kait1',
        'loss_ganeshalingam13_R_kait1',
        'loss_ganeshalingam13_I_kait1',
        'loss_ganeshalingam13_B_kait2',
        'loss_ganeshalingam13_V_kait2',
        'loss_ganeshalingam13_R_kait2',
        'loss_ganeshalingam13_I_kait2',
        'loss_ganeshalingam13_B_kait3',
        'loss_ganeshalingam13_V_kait3',
        'loss_ganeshalingam13_R_kait3',
        'loss_ganeshalingam13_I_kait3'
        'loss_ganeshalingam13_B_kait4',
        'loss_ganeshalingam13_V_kait4',
        'loss_ganeshalingam13_R_kait4',
        'loss_ganeshalingam13_I_kait4',
        'loss_ganeshalingam13_B_nickle',
        'loss_ganeshalingam13_V_nickle',
        'loss_ganeshalingam13_R_nickle',
        'loss_ganeshalingam13_I_nickle')

    # Taken from Table 1
    zero_point = (
        15.304,  # KAIT1 B
        14.913,  # KAIT1 V
        15.357,  # KAIT1 R
        14.686,  # KAIT1 I
        15.361,  # KAIT2 B
        14.914,  # KAIT2 V
        14.975,  # KAIT2 R
        14.452,  # KAIT2 I
        15.332,  # KAIT3 B
        14.921,  # KAIT3 V
        15.008,  # KAIT3 R
        14.457,  # KAIT3 I
        15.249,  # KAIT4 B
        14.922,  # KAIT4 V
        14.973,  # KAIT4 R
        14.439,  # KAIT4 I
        15.224,  # Nickel B
        14.828,  # Nickel V
        14.930,  # Nickel R
        14.703,  # Nickel I
    )

    def __init__(self):
        """Define local and remote paths of data"""

        # Call to parent class defines the self._data_dir attribute
        # All data should be downloaded to / read from that directory
        super().__init__()

        # Define data urls
        self._table_3_url = 'http://heracles.astro.berkeley.edu/sndb/static/LOSS/table3_full.txt'
        self._photometry_url = 'http://heracles.astro.berkeley.edu/sndb/static/LOSS/loss.phot.natural.table.txt'
        self._filter_url = 'http://heracles.astro.berkeley.edu/sndb/static/LOSS/transmission_curves.tar'

        # Local data paths
        self._table_3_path = self._table_dir / 'table3.dat'
        self._photometry_path = self._data_dir / 'photometry.txt'
        self._filter_dir = self._data_dir / 'filters'

    def _load_table(self, table_id: int) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        table_path = self._table_dir / f'table{table_id}.dat'
        table = Table.read(table_path, format='ascii', names=[
            'SN name', 'Redshift in CMB frame', 'm_{B}', 'm_{B} err', 'x_{1}',
            'x_{1} err', 'c', 'c err', 'mu', 'mu_err', 'Sample Name',
            'Reference'], delimiter='  ')

        table = Table(table, masked=True)  # Convert to a masked table
        for col in table.columns.values():
            col.mask = col == 99.999

        return table

    @lru_cache()
    def _load_photometry(self) -> Table:
        """Load photometry data

        Returns:
            An astropy table
        """

        return Table.read(
            self._photometry_path, format='ascii',
            names=['SN', 'MJD', 'Filter', 'Mag', 'Mag err', 'Telescope System']
        )

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        return sorted(np.unique(self._load_photometry()['SN']))

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        photometry = self._load_photometry()
        object_data = photometry[photometry['SN'] == obj_id]

        if format_table:
            zp_dict = dict(zip(self.band_names, self.zero_point))
            bands, zp = [], []
            for row in object_data:
                band = f'loss_ganeshalingam13_{row["Filter"]}_{row["Telescope System"].lower()}'
                bands.append(band)
                zp.append(zp_dict[band])

            object_data['time'] = utils.convert_to_jd(object_data['MJD'], 'mjd')
            object_data['band'] = bands
            object_data['zp'] = zp
            object_data['flux'] = 10 ** ((object_data['Mag'] - object_data['zp']) / -2.5)
            object_data['fluxerr'] = (np.log(10) / -2.5) * object_data['flux'] * object_data['Mag err']
            object_data['zpsys'] = 'Landolt'
            object_data.remove_columns(['Mag', 'Mag err'])

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

        urls = (self._table_3_url, self._photometry_url)
        paths = (self._table_3_path, self._photometry_path)
        for file_url, file_path in zip(urls, paths):
            utils.download_file(
                url=file_url,
                destination=file_path,
                force=force,
                timeout=timeout
            )

        utils.download_tar(
            url=self._filter_url,
            out_dir=self._filter_dir,
            skip_exists=self._filter_dir,
            mode='r',
            force=force,
            timeout=timeout
        )
