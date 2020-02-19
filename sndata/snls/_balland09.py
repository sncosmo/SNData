#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the SNLS Balland09 API"""

import os
from pathlib import Path

from astropy.coordinates import Angle
from astropy.io import ascii
from astropy.table import Table, vstack

from .. import _utils as utils
from .._base import DataRelease
from ..exceptions import InvalidObjId


def fix_balland09_cds_readme(readme_path):
    """Fix typos in the Balland 2009 CDS Readme so it is machine parsable

    Args:
        readme_path: Path of the README file to fix
    """

    # The downloaded files in this case are readonly, so we change permissions
    os.chmod(readme_path, 438)

    with open(readme_path, 'r+') as data_in:
        lines = data_in.readlines()
        lines[112] = lines[112].replace('? ', '?=- ')

        data_in.seek(0)
        data_in.writelines(lines)


class Balland09(DataRelease):
    """The ``Ballan09`` class  provides access to to the three year data 
    release of the Supernova Legacy Survey (SNLS) performed by the 
    Canada-France-Hawaï Telescope (CFHT). It includes 139 spectra of 124 
    Type Ia supernovae that range from z = 0.149 to z = 1.031 and have an 
    average redshift of z = 0.63 +/- 0.02. (Source: Balland et al. 2009)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    # General metadata (Required)
    survey_name = 'Supernova Legacy Survey'
    survey_abbrev = 'SNLS'
    release = 'Balland09'
    survey_url = 'http://supernovae.in2p3.fr/~balland/VltRelease/'
    data_type = 'spectroscopic'
    publications = ('Balland et al. 2009',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2009A%26A...507...85B/abstract'

    def __init__(self):
        # Define local paths of published data
        self._find_or_create_data_dir()
        self._spectra_dir = self.data_dir / 'spectra'  # DR1 spectra
        self._table_dir = self.data_dir / 'tables'  # DR3 paper tables

        # Define urls for remote data
        self._phase_spectra_url = 'http://supernovae.in2p3.fr/~balland/VltRelease/PHASE_spec_Balland09.tar.gz'
        self._snonly_spectra_url = 'http://supernovae.in2p3.fr/~balland/VltRelease/snonly_spec_Balland09.tar.gz'
        self._table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/A+A/507/85'

    def _get_available_ids(self):
        """Return a list of target object IDs for the current survey"""

        files = self._spectra_dir.glob('*.dat')
        ids = (Path(f).name.split('_')[1] for f in files)
        return sorted(set(ids))

    def _get_balland_meta(self, obj_id):
        """Get the ra, dec, redshift and redshift error for a Balland09 SN

        Args:
            obj_id (str): The Id of the Supernova
        """

        # Get Coordinates
        table1 = self.load_table(1)
        object_data = table1[table1['SN'] == obj_id][0]

        ra_hourangle = (object_data['RAh'], object_data['RAm'], object_data['RAs'])
        ra_deg = Angle(ra_hourangle, unit='hourangle').to('deg')

        sign = -1 if object_data['DE-'] == '-' else 1
        dec_deg = (
                sign * object_data['DEd'] +  # Already in degrees
                object_data['DEm'] / 60 +  # arcmin to degrees
                object_data['DEs'] / 60 / 60  # arcesc to degrees
        )

        # Get redshift
        table2 = self.load_table(2)
        object_data = table2[table2['SN'] == obj_id][0]
        z = object_data['z']
        z_err = object_data['e_z']

        return ra_deg.value, dec_deg, z, z_err

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

        tables = []
        for fpath in self._spectra_dir.glob(f'*_{obj_id}_*_Balland_etal_09.dat'):
            data_table = Table.read(
                fpath,
                names=['pixel', 'wavelength', 'flux', 'fluxerr'],
                format='ascii.basic',
                comment='[#]|[@]'
            )

            data_table['type'] = fpath.name.split('_')[0].lower()
            data_table['phase'] = float(data_table.meta['comments'][7].split()[-1])
            tables.append(data_table)

        ra, dec, z, z_err = self._get_balland_meta(obj_id)
        out_table = vstack(tables)

        out_table.meta['obj_id'] = obj_id
        out_table.meta['ra'] = ra
        out_table.meta['dec'] = dec
        out_table.meta['z'] = z
        out_table.meta['z_err'] = z_err
        del out_table.meta['comments']

        return out_table

    def download_module_data(self, force: bool = False):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data (Default: False)
        """

        # Download data tables
        if (force or not self._table_dir.exists()) and utils.check_url(
                self._table_url):
            print('Downloading data tables...')
            utils.download_tar(
                url=self._table_url,
                out_dir=self._table_dir,
                mode='r:gz')

        fix_balland09_cds_readme(self._table_dir / 'ReadMe')

        # Download spectra
        if (force or not self._spectra_dir.exists()):
            spec_urls = self._phase_spectra_url, self._snonly_spectra_url
            names = 'combined', 'supernova only'

            for spectra_url, data_name in zip(spec_urls, names):
                if utils.check_url(spectra_url):
                    print(f'Downloading {data_name} spectra...')
                    utils.download_tar(
                        url=spectra_url,
                        out_dir=self._spectra_dir,
                        mode='r:gz')
