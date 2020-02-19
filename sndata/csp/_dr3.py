#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the CSP DR3 API"""

import numpy as np
from astropy.io import ascii
from astropy.table import Table

from sndata import _utils as utils
from sndata._base import DataRelease
from ..exceptions import InvalidObjId


def parse_snoopy_data(path):
    """Return data from a snoopy file as an astropy table

    Args:
        path (str): The file path of a snoopy input file

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


def fix_cds_readme(lines):
    """Fix typos in the DR3 CDS Readme so it is machine parsable

    Argument is modified in-place

    Args:
        lines (list): Lines read from the CDS file
    """

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


class DR3(DataRelease):
    """The DR3 class provides access to data from the third data release of
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

    Attributes:
        - survey_name
        - release
        - survey_abbrev
        - survey_url
        - data_type
        - publications
        - ads_url

    Methods:
        - delete_module_data
        - download_module_data
        - get_available_ids
        - get_available_tables
        - get_data_for_id
        - iter_data
        - load_table
    """

    survey_name = 'Carnegie Supernova Project'
    survey_abbrev = 'CSP'
    release = 'dr3'
    survey_url = 'https://csp.obs.carnegiescience.edu/news-items/csp-dr3-photometry-released'
    data_type = 'photometric'
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

    lambda_effective = (
        3639.3, 4765.1, 6223.3, 7609.2, 4350.6, 5369.6, 5401.4,
        5375.2, 10350.8, 12386.5, 12356.3, 16297.7, 10439.8,
        12383.2, 16282.8)

    def __init__(self):
        # Define local paths of published data
        self._find_or_create_data_dir()
        self.photometry_dir = self.data_dir / 'DR3'  # DR3 Light Curves
        self.filter_dir = self.data_dir / 'filters'  # DR3 Filters
        self.table_dir = self.data_dir / 'tables'  # DR3 paper tables

        # Define urls for remote data
        self.photometry_url = 'https://csp.obs.carnegiescience.edu/data/CSP_Photometry_DR3.tgz'
        self.filter_url = 'https://csp.obs.carnegiescience.edu/data/'
        self.table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/AJ/154/211'

        # Filter information
        self.filter_file_names = (
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

        self.instrument_offsets = {
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

    def _get_available_tables(self):
        """Get available Ids for tables published by the paper for this data
        release"""

        file_list = self.table_dir.glob('*.dat')
        return sorted(int(path.stem.strip('table')) for path in file_list)

    def _load_table(self, table_id):
        """Return a table from the data paper for this survey / data

        Args:
            table_id: The published table number or table name
        """

        readme_path = self.table_dir / 'ReadMe_formatted'
        table_path = self.table_dir / f'table{table_id}.dat'
        if table_id not in self.get_available_tables():
            raise ValueError(f'Table {table_id} is not available.')

        data = ascii.read(str(table_path), format='cds', readme=str(readme_path))
        description = utils.read_vizier_table_descriptions(readme_path)[table_id]
        data.meta['description'] = description
        return data

    def _get_available_ids(self):
        """Return a list of target object IDs for the current survey"""

        files = self.photometry_dir.glob('*.txt')
        return sorted(f.stem.split('_')[0].lstrip('SN') for f in files)

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

        # Read data file for target
        file_path = self.photometry_dir / f'SN{obj_id}_snpy.txt'
        data_table = parse_snoopy_data(file_path)
        data_table.meta['obj_id'] = data_table.meta['obj_id'].lstrip('SN')

        if format_table:
            # Convert band names to package standard
            data_table['band'] = 'csp_dr3_' + data_table['band']

            offsets = np.array([self.instrument_offsets[b] for b in data_table['band']])
            data_table['mag'] += offsets

            # Add flux values
            data_table['zp'] = self._get_zp_for_bands(data_table['band'])
            data_table['zpsys'] = np.full(len(data_table), 'ab')
            data_table['flux'] = 10 ** ((data_table['mag'] - data_table['zp']) / -2.5)
            data_table['fluxerr'] = np.log(10) * data_table['flux'] * data_table['mag_err'] / 2.5

        return data_table

    def download_module_data(self, force: bool = False):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data (Default: False)
        """

        # Download data tables
        if (force or not self.table_dir.exists()) \
                and utils.check_url(self.table_url):
            print('Downloading data tables...')
            utils.download_tar(
                url=self.table_url,
                out_dir=self.table_dir,
                mode='r:gz')

            # Fix formatting of CDS Readme
            with open(self.table_dir / 'ReadMe') as ofile:
                lines = ofile.readlines()

            fix_cds_readme(lines)
            with open(self.table_dir / 'ReadMe_formatted', 'w') as ofile:
                ofile.writelines(lines)

        # Download photometry
        if (force or not self.photometry_dir.exists()) \
                and utils.check_url(self.photometry_url):
            print('Downloading photometry...')
            utils.download_tar(
                url=self.photometry_url,
                out_dir=self.data_dir,
                mode='r:gz')

        # Download filters
        if (force or not self.filter_dir.exists()) \
                and utils.check_url(self.filter_url):

            print('Downloading filters...')
            for file_name in self.filter_file_names:
                utils.download_file(
                    url=self.filter_url + file_name,
                    out_file=self.filter_dir / file_name)
