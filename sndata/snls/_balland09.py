#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the SNLS Balland09 API"""

import os
from pathlib import Path

from astropy.table import Table, vstack

from .. import utils
from ..base_classes import DefaultParser, SpectroscopicRelease
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


class Balland09(SpectroscopicRelease, DefaultParser):
    """The ``Balland09`` class  provides access to to the three year data
    release of the Supernova Legacy Survey (SNLS) performed by the
    Canada-France-Hawaii Telescope (CFHT). It includes 139 spectra of 124
    Type Ia supernovae that range from z = 0.149 to z = 1.031 and have an
    average redshift of z = 0.63 +/- 0.02. (Source: Balland et al. 2009)

    Deviations from the standard UI:
        - Time values returned in units of phase and not observed Julian date.

    Cuts on returned data:
        - None
    """

    # General metadata (Required)
    survey_name = 'Supernova Legacy Survey'
    survey_abbrev = 'SNLS'
    release = 'Balland09'
    survey_url = 'http://supernovae.in2p3.fr/~balland/VltRelease/'
    publications = ('Balland et al. 2009',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2009A%26A...507...85B/abstract'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()

        # Local paths
        self._spectra_dir = self._data_dir / 'spectra'  # DR1 spectra
        self._table_dir = self._data_dir / 'tables'  # DR3 paper tables

        # Define urls for remote data
        self._phase_spectra_url = 'http://supernovae.in2p3.fr/~balland/VltRelease/PHASE_spec_Balland09.tar.gz'
        self._snonly_spectra_url = 'http://supernovae.in2p3.fr/~balland/VltRelease/snonly_spec_Balland09.tar.gz'
        self._table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/A+A/507/85'

    def _get_available_ids(self):
        """Return a list of target object IDs for the current survey"""

        # Use recursive glob since the data files are in sub directories
        files = self._spectra_dir.rglob('*.dat')
        ids = (Path(f).name.split('_')[1] for f in files)
        return sorted(set(ids))

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

        tables = []
        for fpath in self._spectra_dir.rglob(f'*_{obj_id}_*_Balland_etal_09.dat'):
            data_table = Table.read(
                fpath,
                names=['pixel', 'wavelength', 'flux', 'fluxerr'],
                format='ascii.basic',
                comment='[#]|[@]'
            )

            data_table['type'] = fpath.name.split('_')[0].lower()
            data_table['phase'] = float(data_table.meta['comments'][7].split()[-1])
            tables.append(data_table)

        # Get object coordinates
        table1 = self.load_table(1)
        table1_object_data = table1[table1['SN'] == obj_id][0]
        ra, dec = utils.hourangle_to_degrees(
            rah=table1_object_data['RAh'],
            ram=table1_object_data['RAm'],
            ras=table1_object_data['RAs'],
            dec_sign=table1_object_data['DE-'],
            decd=table1_object_data['DEd'],
            decm=table1_object_data['DEm'],
            decs=table1_object_data['DEs']
        )

        # Get object redshift
        # Get redshift
        table2 = self.load_table(2)
        table2_object_data = table2[table2['SN'] == obj_id][0]
        z = table2_object_data['z']
        z_err = table2_object_data['e_z']

        out_table = vstack(tables)
        out_table.meta['obj_id'] = obj_id
        out_table.meta['ra'] = ra
        out_table.meta['dec'] = dec
        out_table.meta['z'] = z
        out_table.meta['z_err'] = z_err
        del out_table.meta['comments']

        return out_table

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        utils.download_tar(
            url=self._table_url,
            out_dir=self._table_dir,
            skip_exists=self._table_dir,
            mode='r:gz',
            force=force
        )

        readme_path = self._table_dir / 'ReadMe'
        if readme_path.exists():
            fix_balland09_cds_readme(readme_path)

        # Download both kinds of spectra
        spec_urls = self._phase_spectra_url, self._snonly_spectra_url
        names = 'combined', 'sn_only'
        for spectra_url, data_name in zip(spec_urls, names):
            utils.download_tar(
                url=spectra_url,
                out_dir=self._spectra_dir / data_name,
                skip_exists=self._spectra_dir / data_name,
                mode='r:gz',
                force=force,
                timeout=timeout
            )
