#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the CSP DR1 API"""

import os
from pathlib import Path

import numpy as np
from astropy.io import ascii
from astropy.table import Column, Table, vstack

from sndata import _utils as utils
from sndata._base import DataRelease


def _read_file(path):
    """Read a file path of spectroscopic data from CSP DR1

    Args:
        path (str or Path): Path of file to read

    Returns:
        The data of maximum for the observed target
        The redshift of the target
        An astropy table with file data and meta data
    """

    # Handle the single file with a different data model:
    # There are three columns instead of two
    path = Path(path)
    if path.stem == 'SN07bc_070409_b01_BAA_IM':
        data = Table.read(
            path, format='ascii', names=['wavelength', 'flux', '_'])

        data.remove_column('_')

    else:
        data = Table.read(
            path, format='ascii', names=['wavelength', 'flux'])

    # Get various data from the table meta data
    file_comments = data.meta['comments']
    redshift = float(file_comments[1].lstrip('Redshift: '))
    max_date = float(file_comments[2].lstrip('JDate_of_max: '))
    obs_date = float(file_comments[3].lstrip('JDate_of_observation: '))
    epoch = float(file_comments[4].lstrip('Epoch: '))

    # Add remaining columns. These values are constant for a single file
    # (i.e. a single spectrum) but vary across files (across spectra)
    _, _, w_range, telescope, instrument = path.stem.split('_')
    date_col = Column(data=np.full(len(data), obs_date), name='date')
    epoch_col = Column(data=np.full(len(data), epoch), name='epoch')
    wr_col = Column(data=np.full(len(data), w_range), name='wavelength_range')
    tel_col = Column(data=np.full(len(data), telescope), name='telescope')
    inst_col = Column(data=np.full(len(data), instrument), name='instrument')
    data.add_columns([date_col, epoch_col, wr_col, tel_col, inst_col])

    # Ensure dates are in JD format
    data['date'] = utils.convert_to_jd(data['date'])

    return max_date, redshift, data


class DR1(DataRelease):
    """The DR1 class provides access to spectra from the first release of optical
    spectroscopic data of low-redshift Type Ia supernovae (SNe Ia) by the Carnegie
    Supernova Project. It includes 604 previously unpublished spectra of 93 SNe Ia.
    The observations cover a range of phases from 12 days before to over 150 days
    after the time of B-band maximum light. (Source: Folatelli et al. 2013)

    Deviations from the standard UI:
      - This module provides spectroscopic data and as such the ``band_names``,
        and ``lambda_effective`` attributes are not available.

    Cuts on returned data:
      - None
    """

    # General metadata
    survey_name = 'Carnegie Supernova Project'
    release = 'DR1'
    survey_abbrev = 'CSP'
    survey_url = 'https://csp.obs.carnegiescience.edu/news-items/CSP_spectra_DR1'
    data_type = 'spectroscopic'
    publications = ('Folatelli et al. 2013',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2013ApJ...773...53F/abstract'

    def __init__(self):
        if 'SNDATA_DIR' in os.environ:
            self.data_dir = utils.create_data_dir(self.survey_name, self.release)

        else:
            self.data_dir = Path(__file__).resolve().parent / 'data'

        # Define local paths of published data
        self.spectra_dir = self.data_dir / 'CSP_spectra_DR1'  # DR1 spectra
        self.table_dir = self.data_dir / 'tables'  # DR3 paper tables

        # Define urls for remote data
        self.spectra_url = 'https://csp.obs.carnegiescience.edu/data/CSP_spectra_DR1.tgz'
        self.table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/ApJ/773/53'

    # noinspection PyUnusedLocal
    def _register_filters(self, force=False):
        """Register filters for this survey / data release with SNCosmo

        Args:
            force (bool): Whether to re-register a band if already registered
        """

        raise ValueError(
            f'{self.release} {self.survey_abbrev} is a spectroscopic '
            'data release and has no filters to register.'
        )

    #@utils.require_data_path(self.table_dir)
    def _get_available_tables(self):
        """Get table numbers for machine readable tables published in the paper
        for this data release"""

        table_nums = []
        for f in self.table_dir.rglob('table*.dat'):
            table_number = f.stem.lstrip('table')
            table_nums.append(int(table_number))

        return sorted(table_nums)

    #@utils.require_data_path(self.table_dir)
    def _load_table(self, table_id):
        """Load a table from the data paper for this survey / data

        See ``get_available_tables`` for a list of valid table IDs.

        Args:
            table_id (int, str): The published table number or table name
        """

        readme_path = self.table_dir / 'ReadMe'
        table_path = self.table_dir / f'table{table_id}.dat'
        if not table_path.exists:
            raise ValueError(f'Table {table_id} is not available.')

        data = ascii.read(str(table_path), format='cds',
                          readme=str(readme_path))
        description = utils.read_vizier_table_descriptions(readme_path)[
            table_id]
        data.meta['description'] = description
        return data

    #@utils.require_data_path(self.spectra_dir)
    def _get_available_ids(self):
        """Return a list of target object IDs for the current survey

        Returns:
            A list of object IDs as strings
        """

        files = self.spectra_dir.glob('SN*.dat')
        ids = ('20' + Path(f).name.split('_')[0].lstrip('SN') for f in files)
        return sorted(set(ids))

    # noinspection PyUnusedLocal
    #@utils.require_data_path(self.spectra_dir)
    def _get_data_for_id(self, obj_id, format_table=True):
        """Returns data for a given object ID

        See ``get_available_ids()`` for a list of available ID values.

        Args:
            obj_id        (str): The ID of the desired object
            format_table (bool): Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        out_table = Table(
            names=['date', 'wavelength', 'flux', 'epoch', 'wavelength_range',
                   'telescope', 'instrument'],
            dtype=[float, float, float, float, 'U3', 'U3', 'U2']
        )

        files = self.spectra_dir.rglob(f'SN{obj_id[2:]}_*.dat')
        if not files:
            raise ValueError(f'No data found for obj_id {obj_id}')

        for path in files:
            max_date, redshift, spectral_data = _read_file(path)
            out_table = vstack([out_table, spectral_data])

            out_table.meta['obj_id'] = obj_id
            out_table.meta['ra'] = None
            out_table.meta['dec'] = None
            out_table.meta['z'] = redshift
            out_table.meta['z_err'] = None
            del out_table.meta['comments']

            return out_table

    def download_module_data(self, force=False):
        """Download data for the current survey / data release

        Args:
            force (bool): Re-Download locally available data (Default: False)
        """

        # Download data tables
        if (force or not self.table_dir.exists()) \
                and utils.check_url(self.table_url):

            print('Downloading data tables...')
            utils.download_tar(
                url=self.table_url,
                out_dir=self.table_dir,
                mode='r:gz')

        # Download spectra
        if (force or not self.spectra_dir.exists()) \
                and utils.check_url(self.spectra_url):

            print('Downloading spectra...')
            utils.download_tar(
                url=self.spectra_url,
                out_dir=self.data_dir,
                mode='r:gz')
