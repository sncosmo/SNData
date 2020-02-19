#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the SDSS Sako18 API"""

import tarfile
import zipfile
from itertools import product
from urllib.parse import urljoin

import numpy as np
from astropy.table import Column, Table

from .. import _utils as utils
from .._base import DataRelease
from ..exceptions import InvalidObjId


@np.vectorize
def _construct_band_name(filter_id, ccd_id):
    """Return the sncosmo band name given filter and CCD ID

    Args:
        filter_id (int): Filter index 1 through 5 for 'ugriz'
        ccd_id    (int): Column number 1 through 6

    Args:
        The name of the filter registered with sncosmo
    """

    return f'sdss_sako18_{"ugriz"[filter_id]}{ccd_id}'


def _format_sncosmo_table(data_table):
    """Format a data table for use with SNCosmo

    Args:
        data_table (Table): A data table returned by ``get_data_for_id``

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


class Sako18(DataRelease):
    """<Describe the data set> (Source: <Cite a publication>)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None

    Attributes:
        - survey_name
        - release
        - survey_abbrev
        - survey_url
        - data_type
        - publications
        - ads_url
        - band_names
        - zero_point
        - lambda_effective

    Methods:
        - delete_module_data
        - download_module_data
        - get_available_ids
        - get_available_tables
        - get_data_for_id
        - iter_data
        - load_table
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
    lambda_effective = (
        3551, 3551, 3551, 3551, 3551, 3551,
        4686, 4686, 4686, 4686, 4686, 4686,
        6166, 6166, 6166, 6166, 6166, 6166,
        7480, 7480, 7480, 7480, 7480, 7480,
        8932, 8932, 8932, 8932, 8932, 8932
    )

    def __init__(self):
        # Define local paths of published data
        self._find_or_create_data_dir()
        self._filter_dir = self.data_dir / 'doi_2010_filters/'  # Transmission filters
        self._table_dir = self.data_dir / 'tables/'  # Tables from the published paper
        self._smp_dir = self.data_dir / 'SMP_Data/'  # SMP data files (photometric light-curves)
        self._snana_dir = self.data_dir / 'SDSS_dataRelease-snana/'  # SNANA files including list of outliers
        self._outlier_path = self._snana_dir / 'SDSS_allCandidates+BOSS/SDSS_allCandidates+BOSS.IGNORE'  # Outlier data
        self._spectra_dir = self.data_dir / 'Spectra_txt'  # spectra files
        self._spectra_zip = self.data_dir / 'Spectra_txt.zip'  # compressed spectra files

        self._filter_file_names = tuple(f'{b}{c}.dat' for b, c in product('ugriz', '123456'))
        self._table_names = 'master_data.txt', 'Table2.txt', 'Table9.txt', 'Table11.txt', 'Table12.txt'

        # Define urls and file names for remote data
        self._filter_url = 'http://www.ioa.s.u-tokyo.ac.jp/~doi/sdss/'

        self._base_url = 'https://portal.nersc.gov/project/dessn/SDSS/dataRelease/'
        self._smp_url = urljoin(self._base_url, 'SMP_Data.tar.gz')
        self._snana_url = urljoin(self._base_url, 'SDSS_dataRelease-snana.tar.gz')
        self._spectra_url = urljoin(self._base_url, 'Spectra.tar.gz')

    def get_available_tables(self):
        """Get table numbers for machine readable tables published in the paper
        for this data release"""

        utils.require_data_path(self._table_dir)

        table_names = []
        for f in self._table_dir.glob('*.txt'):
            table_num = f.stem.strip('Table_data')
            if table_num.isnumeric():
                table_num = int(table_num)

            table_names.append(table_num)

        return sorted(table_names, key=lambda x: 0 if x == 'master' else x)

    @utils.lru_copy_cache(maxsize=None)
    def load_table(self, table_id):
        """Load a table from the data paper for this survey / data

        See ``get_available_tables`` for a list of valid table IDs.

        Args:
            table_id (int, str): The published table number or table name
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

    def get_available_ids(self):
        """Return a list of target object IDs for the current survey

        Returns:
            A list of object IDs as strings
        """

        return sorted(self.load_table('master')['CID'])

    def get_outliers(self):
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
    def _get_data_for_id(self, obj_id: str, format_table: bool = True):
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

    def download_module_data(self, force=False):
        """Download data for the current survey / data release

        Args:
            force (bool): Re-Download locally available data (Default: False)
        """

        # Photometry
        if (force or not self._smp_dir.exists()) and utils.check_url(self._smp_url):
            print('Downloading SMP data...')
            utils.download_tar(
                url=self._smp_url,
                out_dir=self.data_dir,
                mode='r:gz')

        # SNANA files - including files specifying "bad" photometry data points
        if (force or not self._snana_dir.exists()) and utils.check_url(self._snana_url):
            print('Downloading SNANA data...')
            utils.download_tar(
                url=self._snana_url,
                out_dir=self.data_dir,
                mode='r:gz')

            # Unzip file listing "bad" photometry
            outlier_archive = self._snana_dir / 'SDSS_allCandidates+BOSS.tar.gz'
            with tarfile.open(str(outlier_archive), mode='r:gz') as data:
                data.extractall(str(outlier_archive.parent))

        # Tables from the published paper
        print_tables = True  # Whether to print the status
        if utils.check_url(self._base_url):
            for file_name in self._table_names:

                out_path = self._table_dir / file_name
                if force or not out_path.exists():
                    if print_tables:
                        print(f'Downloading tables...')
                        print_tables = False

                    utils.download_file(
                        url=self._base_url + file_name,
                        out_file=out_path
                    )

        # Photometric filters
        print_photometric = True
        if utils.check_url(self._filter_url):
            for file_name in self._filter_file_names:

                out_path = self._filter_dir / file_name
                if force or not out_path.exists():
                    if print_photometric:
                        print(f'Downloading filters...')
                        print_photometric = False

                    utils.download_file(
                        url=self._filter_url + file_name,
                        out_file=out_path
                    )

        # if (force or not meta.spectra_dir.exists()) \
        #         and utils.check_url(meta.spectra_url):
        #     print('Downloading spectra...')
        #     utils.download_tar(
        #         url=meta.spectra_url,
        #         out_dir=meta.data_dir,
        #         mode='r:gz')

        # Spectral data parsing requires IRAF so we use preparsed data instead
        if force or not self._spectra_dir.exists():
            print('Unzipping spectra...')
            with zipfile.ZipFile(self._spectra_zip, 'r') as zip_ref:
                zip_ref.extractall(self.data_dir)
