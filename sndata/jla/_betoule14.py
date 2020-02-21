#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the JLA Betoule14 API"""

import logging
from typing import List

import numpy as np
import sncosmo
from astropy.io import ascii, fits
from astropy.table import Table

from .. import _utils as utils
from ..base_classes import PhotometricRelease
from ..exceptions import InvalidObjId

log = logging.getLogger(__name__)


class Betoule14(PhotometricRelease):
    """The ``Betoule14`` module provides access to light-curves used in a joint
    analysis of type Ia supernova (SN Ia) observations obtained by the SDSS-II
    and SNLS collaborations. The data set includes several low-redshift samples
    (z<0.1), all 3 seasons from the SDSS-II (0.05 < z < 0.4), and 3 years from
    SNLS (0.2 <z < 1) and totals 740 spectroscopically confirmed type Ia
    supernovae with high quality light curves. (Source: Betoule et al. 2014)

    This data set includes observations taken in the pre 2015 MegaCam filter
    set used by the Canada-France-Hawaii Telescope (CFHT). These filters were
    measured at multiple positions by both the observing team and manufacturer.
    Transmission functions registered by this module represent the average
    transmission across the filter as reported by the manufacturer.

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    # General metadata
    survey_name = 'Joint Light-curve Analysis'
    survey_abbrev = 'JLA'
    release = 'Betoule14'
    survey_url = 'http://supernovae.in2p3.fr/sdss_snls_jla/ReadMe.html'
    publications = ('Betoule et al. (2014)',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2014A%26A...568A..22B/abstract'

    # Photometric metadata (Required for photometric data, otherwise delete)

    band_names = (
        'jla_betoule14_4SHOOTER2::B',
        'jla_betoule14_4SHOOTER2::I',
        'jla_betoule14_4SHOOTER2::R',
        'jla_betoule14_4SHOOTER2::Us',
        'jla_betoule14_4SHOOTER2::V',
        'jla_betoule14_ACSWF::F606W',
        'jla_betoule14_ACSWF::F775W',
        'jla_betoule14_ACSWF::F850LP',
        'jla_betoule14_KEPLERCAM::B',
        'jla_betoule14_KEPLERCAM::Us',
        'jla_betoule14_KEPLERCAM::V',
        'jla_betoule14_KEPLERCAM::i',
        'jla_betoule14_KEPLERCAM::r',
        'jla_betoule14_MEGACAMPSF::g',
        'jla_betoule14_MEGACAMPSF::i',
        'jla_betoule14_MEGACAMPSF::r',
        'jla_betoule14_MEGACAMPSF::z',
        'jla_betoule14_NICMOS2::F110W',
        'jla_betoule14_NICMOS2::F160W',
        'jla_betoule14_SDSS::g',
        'jla_betoule14_SDSS::i',
        'jla_betoule14_SDSS::r',
        'jla_betoule14_SDSS::u',
        'jla_betoule14_SDSS::z',
        'jla_betoule14_STANDARD::B',
        'jla_betoule14_STANDARD::I',
        'jla_betoule14_STANDARD::R',
        'jla_betoule14_STANDARD::U',
        'jla_betoule14_STANDARD::V',
        'jla_betoule14_SWOPE2::B',
        'jla_betoule14_SWOPE2::V',
        'jla_betoule14_SWOPE2::g',
        'jla_betoule14_SWOPE2::i',
        'jla_betoule14_SWOPE2::r',
        'jla_betoule14_SWOPE2::u'
    )

    lambda_effective = (
        4358.25,
        8019.814,
        6558.283,
        3562.166,
        5417.783,
        5957.935,
        7705.673,
        9052.537,
        4355.833,
        3562.166,
        5409.747,
        7674.082,
        6242.36,
        np.nan,
        np.nan,
        np.nan,
        np.nan,
        11399.961,
        16101.54,
        4717.598,
        7506.208,
        6186.798,
        3594.325,
        8918.301,
        4393.265,
        8044.647,
        6545.411,
        3562.166,
        5491.773,
        4405.525,
        5387.569,
        4794.042,
        7630.763,
        6239.341,
        3628.672
    )

    zero_point = (
        15.34721,
        14.465326,
        15.067505,
        14.205682,
        14.97444,
        17.21704,
        16.178942,
        15.833444,
        15.358495,
        14.205682,
        14.951837,
        14.962131,
        15.235409,
        27.045017,
        26.340862,
        26.494886,
        25.310699,
        16.733045,
        15.494573,
        27.5,
        27.5,
        27.5,
        27.5,
        27.5,
        15.277109,
        14.589873,
        15.05484,
        14.205682,
        14.841261,
        14.319437,
        14.522684,
        15.127543,
        14.777211,
        14.909701,
        13.036368
    )

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()

        # Local paths
        self._photometry_dir = self._data_dir / 'jla_light_curves'  # Photometry data
        self._table_dir = self._data_dir / 'tables'  # Vizier tables
        self._filter_path = self._data_dir / 'cfht_filters.txt'

        # Define urls for remote data
        self._photometry_url = 'http://supernovae.in2p3.fr/sdss_snls_jla/jla_light_curves.tgz'
        self._table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/A+A/568/A22'
        self._filter_url = 'http://www.cfht.hawaii.edu/Instruments/Imaging/Megacam/data.MegaPrime/MegaCam_Filters_data_SAGEM.txt'

    def register_filters(self, force: bool = False):
        """Register filters for this survey / data release with SNCosmo

        Args:
            force: Re-register a band if already registered (Default: False)
        """

        utils.require_data_path(self._filter_path)
        data_arr = np.genfromtxt(self._filter_path, skip_header=1)
        filt_table = Table(data_arr, names=['wave', 'u', 'g', 'r', 'i', 'z'])
        filt_table['wave'] *= 10  # Convert nm to angstroms

        # Bands are already registered in sncosmo under a different name.
        # We register them using the package standardized name
        for new_band_name in self.band_names:
            built_in_name = new_band_name.split('_')[-1]

            # MEGACAMPSF are radius dependant
            if 'MEGACAMPSF' in built_in_name:
                trans = filt_table[built_in_name[-1].lower()]
                new_band = sncosmo.Bandpass(filt_table['wave'], trans)

            else:
                built_in_band = sncosmo.get_bandpass(built_in_name)
                new_band = sncosmo.Bandpass(built_in_band.wave,
                                            built_in_band.trans)

            new_band.name = new_band_name
            sncosmo.register(new_band, force=force)

    def get_available_tables(self) -> List[str]:
        """Get available Ids for tables published by the paper for this data
        release"""

        utils.require_data_path(self._table_dir)
        dat_file_list = list(self._table_dir.glob('table*.dat'))
        fits_file_list = list(self._table_dir.glob('table*.fit'))
        file_list = dat_file_list + fits_file_list
        return sorted([str(f).rstrip('.datfit')[-2:] for f in file_list])

    def load_table(self, table_id: str) -> Table:
        """Return a table from the data paper for this survey / data

        Args:
            table_id: The published table number or table name
        """

        if table_id not in self.get_available_tables():
            raise ValueError(f'Table {table_id} is not available.')

        # Tables 2 is a fits file
        if table_id == 'f2':
            with fits.open(self._table_dir / f'table{table_id}.fit') as hdulist:
                data = Table(hdulist[0].data)

            description = 'Covariance matrix of the binned distance modulus'
            data.meta['description'] = description
            return data

        # Remaining tables should be .dat files
        readme_path = self._table_dir / 'ReadMe'
        table_path = self._table_dir / f'table{table_id}.dat'
        data = ascii.read(str(table_path), format='cds', readme=str(readme_path))
        description_dict = utils.read_vizier_table_descriptions(readme_path)
        data.meta['description'] = description_dict[f'{table_id}']
        return data

    def _get_available_ids(self):
        """Return a list of target object IDs for the current survey"""

        utils.require_data_path(self._photometry_dir)
        file_list = self._photometry_dir.glob('*.list')
        return sorted(str(f).split('-')[-1][:-5] for f in file_list)

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

        # Get target meta data
        meta_data = dict()
        path = self._photometry_dir / f'lc-{obj_id}.list'
        with open(path) as infile:
            line = infile.readline()
            while line.startswith('@'):
                split_line = line.lstrip('@').split(' ')
                meta_data[split_line[0]] = split_line[1].rstrip()
                line = infile.readline()

            # Initialize data as an astropy table
            names = ['Date', 'Flux', 'Fluxerr', 'ZP', 'Filter', 'MagSys']
            out_table = Table.read(
                infile.readlines(),
                names=names,
                comment='#|@',
                format='ascii.csv',
                delimiter=' ')

        # Set sncosmo format
        if format_table:
            out_table.rename_column('Date', 'time')
            out_table.rename_column('Flux', 'flux')
            out_table.rename_column('Fluxerr', 'fluxerr')
            out_table.rename_column('Filter', 'band')
            out_table.rename_column('ZP', 'zp')
            out_table.rename_column('MagSys', 'zpsys')

            out_table['time'] = utils.convert_to_jd(out_table['time'])
            out_table['band'] = ['jla_betoule14_' + b for b in
                                 out_table['band']]

        # Add package standard metadata
        ra = meta_data.pop('RA', None)
        dec = meta_data.pop('DEC', None)
        ra = float(ra) if ra is not None else ra
        dec = float(dec) if dec is not None else dec

        out_table.meta['obj_id'] = obj_id
        out_table.meta['ra'] = ra
        out_table.meta['dec'] = dec
        out_table.meta['z'] = float(meta_data.pop('Z_HELIO'))
        out_table.meta['z_err'] = None
        out_table.meta.update(meta_data)

        del out_table.meta['comments']
        del out_table.meta['SN']

        return out_table

    def download_module_data(self, force: bool = False):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data (Default: False)
        """

        # Download data tables
        if (force or not self._table_dir.exists()) \
                and utils.check_url(self._table_url):
            log.info('Downloading data tables...')
            utils.download_tar(
                url=self._table_url,
                out_dir=self._table_dir,
                mode='r:gz')

        # Download Photometry
        if (force or not self._photometry_dir.exists()) \
                and utils.check_url(self._photometry_url):
            log.info('Downloading photometry...')
            utils.download_tar(
                url=self._photometry_url,
                out_dir=self._data_dir,
                mode='r:gz')

        # Download Filters
        if (force or not self._filter_path.exists()) \
                and utils.check_url(self._filter_url):
            log.info('Downloading filters...')
            utils.download_file(url=self._filter_url, out_file=self._filter_path)
