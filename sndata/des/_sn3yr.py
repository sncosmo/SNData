#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the DES SN3YR API"""

from typing import List
from typing import Union

import numpy as np
from astropy.table import Table

from .. import utils
from ..base_classes import DefaultParser, PhotometricRelease
from ..exceptions import InvalidObjId


def _format_sncosmo_table(data_table: Table) -> Table:
    """Format a data table for use with SNCosmo

    Args:
        data_table: A SN3YR table to format

    Returns:
        The same data in a new table following the SNCosmo data model
    """

    out_table = Table()
    out_table.meta = data_table.meta

    out_table['time'] = utils.convert_to_jd(data_table['MJD'])
    out_table['band'] = ['des_sn3yr_' + s for s in data_table['BAND']]
    out_table['flux'] = data_table['FLUXCAL']
    out_table['fluxerr'] = data_table['FLUXCALERR']
    out_table['zp'] = np.full(len(data_table), 27.5)
    out_table['zpsys'] = np.full(len(data_table), 'ab')
    return out_table


class SN3YR(PhotometricRelease, DefaultParser):
    """The ``SN3YR`` class provides access to data from the first public data
    release of the Dark Energy Survey Supernova Program, DES-SN3YR. It includes
    griz light curves of 251 supernovae from the first 3 years of the Dark
    Energy Survey Supernova Program’s (DES-SN) spectroscopically classified
    sample. (Source: Brout et al. 2019)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    # General metadata (Required)
    survey_name = 'Dark Energy Survey'
    survey_abbrev = 'DES'
    release = 'SN3YR'
    survey_url = 'https://des.ncsa.illinois.edu/'
    publications = (
        'Burke et al. 2017',
        'Brout et al. 2019',
        'Brout et al. 2018-SYS'
    )

    ads_url = 'https://ui.adsabs.harvard.edu/abs/2019ApJ...874..106B/abstract'

    # Photometric metadata (Required for photometric data, otherwise delete)
    band_names = (
        'des_sn3yr_g',
        'des_sn3yr_r',
        'des_sn3yr_i',
        'des_sn3yr_z',
        'des_sn3yr_y')

    zero_point = tuple(27.5 for _ in band_names)

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()

        # Local paths
        self._filter_dir = self._data_dir / '01-FILTERS' / 'DECam'
        self._photometry_dir = self._data_dir / '02-DATA_PHOTOMETRY/DES-SN3YR_DES'
        self._fits_dir = self._data_dir / '04-BBCFITS'

        # Define urls for remote data
        _des_url = 'http://desdr-server.ncsa.illinois.edu/despublic/sn_files/y3/tar_files/'
        self._filter_url = _des_url + '01-FILTERS.tar.gz'
        self._photometry_url = _des_url + '02-DATA_PHOTOMETRY.tar.gz'
        self._fits_url = _des_url + '04-BBCFITS.tar.gz'

        self._filter_file_names = (
            'DECam_g.dat',
            'DECam_r.dat',
            'DECam_i.dat',
            'DECam_z.dat',
            'DECam_Y.dat')

    def _get_available_tables(self) -> List[str]:
        """Get Ids for available vizier tables published by this data release"""

        # noinspection SpellCheckingInspection
        return ['SALT2mu_DES+LOWZ_C11.FITRES', 'SALT2mu_DES+LOWZ_G10.FITRES']

    def _load_table(self, table_id: Union[str, int]):
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        if table_id not in self.get_available_tables():
            raise ValueError(f'Table {table_id} is not available.')

        # noinspection SpellCheckingInspection
        data = Table.read(
            str(self._fits_dir / table_id),
            format='ascii',
            data_start=4,
            comment='#',
            exclude_names=['dummy_col'],
            names=['dummy_col', 'CID', 'CIDint', 'IDSURVEY', 'TYPE', 'FIELD',
                   'CUTFLAG_SNANA', 'zHEL', 'zHELERR', 'zCMB', 'zCMBERR',
                   'zHD', 'zHDERR', 'VPEC', 'VPECERR', 'HOST_LOGMASS',
                   'HOST_LOGMASS_ERR', 'SNRMAX1', 'SNRMAX2', 'SNRMAX3',
                   'PKMJD',
                   'PKMJDERR', 'x1', 'x1ERR', 'c', 'cERR', 'mB', 'mBERR', 'x0',
                   'x0ERR', 'COV_x1_c', 'COV_x1_x0', 'COV_c_x0', 'NDOF',
                   'FITCHI2', 'FITPROB', 'RA', 'DECL', 'TGAPMAX', 'TrestMIN',
                   'TrestMAX', 'MWEBV', 'm0obs_i', 'm0obs_r', 'em0obs_i',
                   'em0obs_r',
                   'MU', 'MUMODEL', 'MUERR', 'MUERR_RAW', 'MURES', 'MUPULL',
                   'M0DIF',
                   'ERRCODE', 'biasCor_mu', 'biasCorErr_mu', 'biasCor_mB',
                   'biasCor_x1', 'biasCor_c', 'biasScale_muCOV', 'IDSAMPLE'])

        return data

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        # Load list of all target IDs
        target_list_path = self._photometry_dir / 'DES-SN3YR_DES.LIST'
        file_list = np.genfromtxt(target_list_path, dtype=str)
        return sorted(f.lstrip('des_').rstrip('.dat') for f in file_list)

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
        file_path = self._photometry_dir / f'des_{int(obj_id):08d}.dat'

        # noinspection SpellCheckingInspection
        data = Table.read(
            file_path, format='ascii',
            data_start=27, data_end=-1,
            names=['VARLIST:', 'MJD', 'BAND', 'FIELD', 'FLUXCAL', 'FLUXCALERR',
                   'ZPFLUX', 'PSF', 'SKYSIG', 'GAIN', 'PHOTFLAG', 'PHOTPROB'])

        # Add meta data to table
        with open(file_path) as ofile:
            table_meta_data = ofile.readlines()
            data.meta['obj_id'] = obj_id
            data.meta['ra'] = float(table_meta_data[7].split()[1])
            data.meta['dec'] = float(table_meta_data[8].split()[1])
            data.meta['z'] = float(table_meta_data[13].split()[1])
            data.meta['z_err'] = float(table_meta_data[13].split()[3])
            data.meta['dtype'] = 'photometric'
            del data.meta['comments']

        if format_table:
            data = _format_sncosmo_table(data)

        return data

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        # Download filters
        utils.download_tar(
            url=self._filter_url,
            out_dir=self._data_dir,
            skip_exists=self._filter_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )

        # Download photometry data
        utils.download_tar(
            url=self._photometry_url,
            out_dir=self._data_dir,
            skip_exists=self._photometry_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )

        # Download supplementary tables
        utils.download_tar(
            url=self._fits_url,
            out_dir=self._data_dir,
            skip_exists=self._fits_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )
