#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the CSP DR3 API"""

import os
from typing import List

import numpy as np
from astropy.table import Table

from sndata import utils as utils
from sndata.base_classes import DefaultParser, PhotometricRelease


def parse_snoopy_data(path: str):
    """Return data from a snoopy file as an astropy table

    Args:
        path: The file path of a snoopy input file

    Returns:
        An astropy table with columns 'time', 'band', 'mag', and 'mag_err'
    """

    out_table = Table(
        names=['time', 'band', 'mag', 'mag_err'],
        dtype=[float, object, float, float]
    )

    with open(path) as ofile:
        # Get meta data from first line
        name, z, ra, dec = ofile.readline().split()
        out_table.meta['obj_id'] = name
        out_table.meta['ra'] = float(ra)
        out_table.meta['dec'] = float(dec)
        out_table.meta['z'] = float(z)
        out_table.meta['z_err'] = None

        # Read photometric data from the rest of the file
        band = None
        for line in ofile.readlines():
            line_list = line.split()
            if line.startswith('filter'):
                band = line_list[1]
                continue

            time, mag, mag_err = line_list
            out_table.add_row([time, band, mag, mag_err])

    out_table['time'] = utils.convert_to_jd(out_table['time'])
    return out_table


def fix_dr3_readme(readme_path: str):
    """Fix typos in the DR3 CDS Readme so it is machine parsable

    Args:
        readme_path: Path of the README file to fix
    """

    os.chmod(readme_path, 438)  # Make sure we can edit the file
    with open(readme_path, 'r+') as readme:
        lines = readme.readlines()

        # Mistakes in Table 2
        lines[148] = lines[148].replace('[0.734/2.256]?', '?=-')
        lines[150] = lines[150].replace('[0.036/0.198]?', '?')
        lines[153] = lines[153].replace('Wang et al.', '?=- Wang et al.')
        lines[155] = lines[155].replace('Branch et al.', '?=- Branch et al.')
        lines[161] = lines[161].replace('[-11/66]?', '?=-')

        # Mistakes in Table 3
        lines[186] = lines[186].replace('[53263.77/54960.03]?', '?=-')
        lines[189] = lines[189].replace('[0.06/2.71]?', '?')
        lines[190] = lines[190].replace('[53234.7/55165.94]?', '?=-')
        lines[193] = lines[193].replace('[0.6/1.24]?', '?')
        lines[194] = lines[194].replace('[0.278/1.993]?', '?=-')
        lines[195] = lines[195].replace('[0.01/0.175]?', '?')
        lines[196] = lines[196].replace('[0.734/2.256]?', '?=-')
        lines[198] = lines[198].replace('[0.036/0.198]?', '?')
        lines[199] = lines[199].replace('[0.301/1.188]?', '?=-')
        lines[201] = lines[201].replace('[0.005/1.761]?', '?')
        lines[202] = lines[202].replace('[0.06/1.28]?', '?=-')
        lines[204] = lines[204].replace('[0.06/0.067]?', '?')

        readme.seek(0)
        readme.writelines(lines)


class DR3(PhotometricRelease, DefaultParser):
    """The ``DR3`` class provides access to data from the third data release of
    the Carnegie Supernova Project (CSP) which includes natural-system optical
    (ugriBV) and near-infrared (YJH) photometry of 134 supernovae (SNe) that
    were observed in 2004-2009 as part of the first stage of the Carnegie
    Supernova Project (CSP-I). The sample consists of 123 Type Ia SNe, 5 Type
    Iax SNe, 2 super-Chandrasekhar SN candidates, 2 Type Ia SNe interacting
    with circumstellar matter, and 2 SN 2006bt-like events. The redshifts of
    the objects range from z=0.0037 to 0.0835; the median redshift is 0.0241.
    For 120 (90%) of these SNe, near-infrared photometry was obtained.
    (Source: Krisciunas et al. 2017)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    survey_name = 'Carnegie Supernova Project'
    survey_abbrev = 'CSP'
    release = 'DR3'
    survey_url = 'https://csp.obs.carnegiescience.edu/news-items/csp-dr3-photometry-released'
    publications = ('Krisciunas et al. 2017',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2017AJ....154..278K/abstract'

    _band_names = (
        'u', 'g', 'r', 'i', 'B', 'V0', 'V1',
        'V', 'Y', 'J', 'Jrc2', 'H', 'Ydw', 'Jdw', 'Hdw'
    )

    band_names = tuple(f'csp_dr3_{f}' for f in _band_names)
    zero_point = (
        12.986, 15.111, 14.902, 14.545, 14.328, 14.437, 14.393,
        14.439, 13.921, 13.836, 13.836, 13.510, 13.770, 13.866, 13.502
    )

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()

        # Local paths
        self._photometry_dir = self._data_dir / 'DR3'
        self._filter_dir = self._data_dir / 'filters'
        self._table_dir = self._data_dir / 'tables'

        # Define urls for remote data
        self._photometry_url = 'https://csp.obs.carnegiescience.edu/data/CSP_Photometry_DR3.tgz'
        self._filter_url = 'https://csp.obs.carnegiescience.edu/data/'
        self._table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/AJ/154/211'

        # Filter information
        self._filter_file_names = (
            'u_tel_ccd_atm_ext_1.2.dat',  # u
            'g_tel_ccd_atm_ext_1.2.dat',  # g
            'r_tel_ccd_atm_ext_1.2_new.dat',  # r
            'i_tel_ccd_atm_ext_1.2_new.dat',  # i
            'B_tel_ccd_atm_ext_1.2.dat',  # B
            'V_LC3014_tel_ccd_atm_ext_1.2.dat',  # V0
            'V_LC3009_tel_ccd_atm_ext_1.2.dat',  # V1
            'V_tel_ccd_atm_ext_1.2.dat',  # V
            'Y_SWO_TAM_scan_atm.dat',  # Y
            'J_old_retrocam_swope_atm.dat',  # J
            'J_SWO_TAM_atm.dat',  # Jrc2
            'H_SWO_TAM_scan_atm.dat',  # H
            'Y_texas_DUP_atm.dat',  # Ydw
            'J_texas_DUP_atm.dat',  # Jdw
            'H_texas_DUP_atm.dat'  # Hdw
        )

        self._instrument_offsets = {
            'csp_dr3_u': -0.06,
            'csp_dr3_g': -0.02,
            'csp_dr3_r': -0.01,
            'csp_dr3_i': 0,
            'csp_dr3_B': -0.13,
            'csp_dr3_V': -0.02,
            'csp_dr3_V0': -0.02,
            'csp_dr3_V1': -0.02,
            'csp_dr3_Y': 0.63,
            'csp_dr3_J': 0.91,
            'csp_dr3_Jrc2': 0.90,
            'csp_dr3_H': 1.34,
            'csp_dr3_Ydw': 0.64,
            'csp_dr3_Jdw': 0.90,
            'csp_dr3_Hdw': 1.34
        }

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        files = self._photometry_dir.glob('*.txt')
        return sorted(f.stem.split('_')[0].lstrip('SN') for f in files)

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        # Read data file for target
        file_path = self._photometry_dir / f'SN{obj_id}_snpy.txt'
        data_table = parse_snoopy_data(file_path)
        data_table.meta['obj_id'] = data_table.meta['obj_id'].lstrip('SN')

        if format_table:
            # Convert band names to package standard
            data_table['band'] = 'csp_dr3_' + data_table['band']

            offsets = np.array([self._instrument_offsets[b] for b in data_table['band']])
            data_table['mag'] += offsets

            # Add flux values
            data_table['zp'] = self.get_zp_for_band(data_table['band'])
            data_table['zpsys'] = np.full(len(data_table), 'ab')
            data_table['flux'] = 10 ** ((data_table['mag'] - data_table['zp']) / -2.5)
            data_table['fluxerr'] = np.log(10) * data_table['flux'] * data_table['mag_err'] / 2.5

        return data_table

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
            force=force,
            timeout=timeout
        )

        # Fix formatting of CDS Readme
        readme_path = self._table_dir / 'ReadMe'
        if readme_path.exists():
            fix_dr3_readme(readme_path)

        # Download photometry
        utils.download_tar(
            url=self._photometry_url,
            out_dir=self._data_dir,
            skip_exists=self._photometry_dir,
            mode='r:gz',
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
