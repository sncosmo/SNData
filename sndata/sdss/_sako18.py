#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the SDSS Sako18 API for photometric data"""

import tarfile
from itertools import product
from typing import List, Union
from urllib.parse import urljoin

import numpy as np
from astropy.table import Column, Table

from .. import utils
from ..base_classes import DefaultParser, PhotometricRelease
from ..exceptions import InvalidObjId


@np.vectorize
def _construct_band_name(filter_id: int, ccd_id: int) -> str:
    """Return the sncosmo band name given filter and CCD ID

    Args:
        filter_id: Filter index 1 through 5 for 'ugriz'
        ccd_id: Column number 1 through 6

    Args:
        The name of the filter registered with sncosmo
    """

    return f'sdss_sako18_{"ugriz"[filter_id]}{ccd_id}'


def _format_sncosmo_table(data_table: Table) -> Table:
    """Format a data table for use with SNCosmo

    Args:
        data_table: A data table returned by ``get_data_for_id``

    Returns:
        The same data in a new table following the SNCosmo data model
    """

    # Format table
    if not data_table:
        return Table(
            names=['time', 'band', 'zp', 'flux', 'fluxerr', 'zpsys', 'flag'])

    out_table = Table()
    out_table.meta = data_table.meta

    out_table['time'] = data_table['JD']
    out_table['band'] = _construct_band_name(
        data_table['FILT'], data_table['IDCCD'])

    out_table['zp'] = np.full(len(data_table), 2.5 * np.log10(3631))
    out_table['flux'] = data_table['FLUX'] * 1E-6
    out_table['fluxerr'] = data_table['FLUXERR'] * 1E-6
    out_table['zpsys'] = np.full(len(data_table), 'ab')
    out_table['flag'] = data_table['FLAG']

    return out_table


class Sako18(PhotometricRelease, DefaultParser):
    """The ``Sako18`` class provides access to the **photometric** data release
    of the Sloan Digital Sky Survey-II (SDSS-II) Supernova Survey conducted
    between 2005 and 2007. Light curves are presented for 10,258 variable and
    transient sources discovered through repeat ugriz imaging of SDSS Stripe
    82, a 300 deg2 area along the celestial equator. This data release is
    comprised of all transient sources brighter than r ≃ 22.5 mag with no
    history of variability prior to 2004. (Source: Sako et al. 2018)

    For the spectroscopic data of this data release see the ``sako18spec``
    module.

    Deviations from the standard UI:
        - The ``get_outliers`` method returns a dictionary of observations
          visually flagged by the SDSS team as outliers.

    Cuts on returned data:
        - Data points manually marked as outliers by the SDSS research time
          are not included in returned data tables.
    """

    # General metadata
    survey_name = 'Sloan Digital Sky Survey'
    survey_abbrev = 'SDSS'
    release = 'sako18'
    survey_url = 'https://portal.nersc.gov/project/dessn/SDSS/dataRelease/'
    data_type = 'photometric'
    publications = ('Sako et al. (2018)',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2018PASP..130f4002S/abstract'

    # Photometric metadata (Required for photometric data, otherwise delete)
    # Filter information
    # Effective wavelengths for SDSS filters ugriz in angstroms
    # are available at https://www.sdss.org/instruments/camera/#Filters
    band_names = tuple(f'sdss_sako18_{b}{c}' for b, c in product('ugriz', '123456'))
    zero_point = tuple(2.5 * np.log10(3631) for _ in band_names)

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()

        # Local paths
        self._filter_dir = self._data_dir / 'doi_2010_filters/'  # Transmission filters
        self._table_dir = self._data_dir / 'tables/'  # Tables from the published paper
        self._smp_dir = self._data_dir / 'SMP_Data/'  # SMP data files (photometric light-curves)
        self._snana_dir = self._data_dir / 'SDSS_dataRelease-snana/'  # SNANA files including list of outliers
        self._outlier_path = self._snana_dir / 'SDSS_allCandidates+BOSS/SDSS_allCandidates+BOSS.IGNORE'  # Outlier data

        self._filter_file_names = tuple(f'{b}{c}.dat' for b, c in product('ugriz', '123456'))
        self._table_names = 'master_data.txt', 'Table2.txt', 'Table9.txt', 'Table11.txt', 'Table12.txt'

        # Define urls and file names for remote data
        self._filter_url = 'http://www.ioa.s.u-tokyo.ac.jp/~doi/sdss/'

        self._base_url = 'https://portal.nersc.gov/project/dessn/SDSS/dataRelease/'
        self._smp_url = urljoin(self._base_url, 'SMP_Data.tar.gz')
        self._snana_url = urljoin(self._base_url, 'SDSS_dataRelease-snana.tar.gz')

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

    def _get_available_ids(self):
        """Return a list of target object IDs for the current survey

        Returns:
            A list of object IDs
        """

        return sorted(self.load_table('master')['CID'])

    def get_outliers(self) -> dict:
        """Return a dictionary of data points marked by SDSS II as outliers

        Returns:
            A dictionary {<obj_id>: [<MJD of bad data point>, ...], ...}
        """

        out_dict = dict()
        with open(self._outlier_path) as ofile:
            for line in ofile.readlines():
                if line.startswith('IGNORE:'):
                    line_list = line.split()
                    cid, mjd, band = line_list[1], line_list[2], line_list[3]
                    if cid not in out_dict:
                        out_dict[str(cid)] = []

                    out_dict[str(cid)].append(mjd)

        return out_dict

    # noinspection PyUnusedLocal
    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        if obj_id not in self.get_available_ids():
            raise InvalidObjId()

            # Read in ascii data table for specified object
        file_path = self._smp_dir / f'SMP_{int(obj_id):06d}.dat'
        data = Table.read(file_path, format='ascii')

        # Rename columns using header data from file
        col_names = data.meta['comments'][-1].split()
        for i, name in enumerate(col_names):
            data[f'col{i + 1}'].name = name

        data['JD'] = utils.convert_to_jd(data['MJD'])

        # Add meta data
        master_table = self.load_table('master')
        table_meta_data = master_table[master_table['CID'] == obj_id]
        data.meta['obj_id'] = obj_id
        data.meta['ra'] = table_meta_data['RA'][0]
        data.meta['dec'] = table_meta_data['DEC'][0]
        data.meta['z'] = table_meta_data['zCMB'][0]
        data.meta['z_err'] = table_meta_data['zerrCMB'][0]
        data.meta['dtype'] = 'photometric'
        data.meta['classification'] = table_meta_data['Classification'][0]
        del data.meta['comments']

        outlier_list = self.get_outliers().get(obj_id, [])
        if outlier_list:
            keep_indices = ~np.isin(data['MJD'], outlier_list)
            data = data[keep_indices]

        if format_table:
            data = _format_sncosmo_table(data)

        return data

    def _download_module_data(self, force=False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        # Photometry
        utils.download_tar(
            url=self._smp_url,
            out_dir=self._data_dir,
            skip_exists=self._smp_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )

        # SNANA files - including files specifying "bad" photometry data points
        utils.download_tar(
            url=self._snana_url,
            out_dir=self._data_dir,
            skip_exists=self._snana_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )

        # Unzip file listing "bad" photometry
        outlier_archive = self._snana_dir / 'SDSS_allCandidates+BOSS.tar.gz'
        if outlier_archive.exists():
            with tarfile.open(str(outlier_archive), mode='r:gz') as data:
                data.extractall(str(outlier_archive.parent))

        for file_name in self._table_names:
            utils.download_file(
                url=self._base_url + file_name,
                path=self._table_dir / file_name,
                force=force,
                timeout=timeout
            )

        for file_name in self._filter_file_names:
            utils.download_file(
                url=self._filter_url + file_name,
                path=self._filter_dir / file_name,
                force=force,
                timeout=timeout
            )
