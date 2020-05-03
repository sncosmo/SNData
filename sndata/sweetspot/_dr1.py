#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the Sweetspot DR1 API"""

import tarfile
from pathlib import Path
from typing import List

from astropy.table import Table

from .. import utils
from ..base_classes import PhotometricRelease, DefaultParser

_dr1_files = [
    'CSS121009:011101-172841_CSS121009:011101-172841.Wstd.dat',
    'CSS121114:090202+101800_CSS121114:090202+101800.Wstd.dat',
    'LSQ12fhs_LSQ12fhs.Wstd.dat',
    'LSQ12fmx_LSQ12fmx.Wstd.dat',
    'LSQ13cmt_LSQ13cmt.Wstd.dat',
    'LSQ13cwp_LSQ13cwp.Wstd.dat',
    'PS1-13dkh_PS1-13dkh.Wstd.dat',
    'PTF11moy_PTF11moy.Wstd.dat',
    'PTF11qmo_PTF11qmo.Wstd.dat',
    'PTF13asv_PTF13asv.Wstd.dat',
    'PTF13dad_PTF13dad.Wstd.dat',
    'PTF13ddg_PTF13ddg.Wstd.dat',
    'SN2011fe_SN2011fe.Wstd.dat',
    'SN2011fs_SN2011fs.Wstd.dat',
    'SN2011gf_SN2011gf.Wstd.dat',
    'SN2011io_SN2011io.Wstd.dat',
    'SN2011iy_SN2011iy.Wstd.dat',
    'SN2011jh_SN2011jh.Wstd.dat',
    'SN2012bh_SN2012bh.Wstd.dat',
    'SN2012bo_SN2012bo.Wstd.dat',
    'SN2012bp_SN2012bp.Wstd.dat',
    'SN2012em_SN2012em.Wstd.dat',
    'SN2012fk_SN2012fk.Wstd.dat',
    'SN2012fr_SN2012fr.Wstd.dat',
    'SN2013ar_SN2013ar.Wstd.dat',
    'SN2013bs_SN2013bs.Wstd.dat',
    'SN2013bt_SN2013bt.Wstd.dat',
    'SN2013cs_SN2013cs.Wstd.dat',
    'SN2013fn_SN2013fn.Wstd.dat',
    'iPTF13dge_iPTF13dge.Wstd.dat',
    'iPTF13dkl_iPTF13dkl.Wstd.dat',
    'iPTF13dkx_iPTF13dkx.Wstd.dat',
    'iPTF13ebh_iPTF13ebh.Wstd.dat']


class DR1(PhotometricRelease, DefaultParser):
    """SweetSpot is a 3 yr National Optical Astronomy Observatory (NOAO)
    survey program to observe Type Ia supernovae (SNe Ia) in the smooth Hubble
    flow. DR1 includes data from the first half of this survey, including
    SNe Ia observed in the rest-frame near-infrared (NIR) in the range
    0.02 < z < 0.09. Because many observed supernovae require host-galaxy
    subtraction from templates taken in later semesters, this release contains
    only the 186 NIR (JHK s ) data points for the 33 SNe Ia that do not require
    host-galaxy subtraction. (Source: Weyant et al. 2018)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    survey_name = 'Sweetspot'
    survey_abbrev = 'sweetspot'
    release = 'DR1'
    survey_url = 'https://mwvgroup.github.io/SweetSpot/'
    publications = ('Weyant et al. 2018',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2018AJ....155..201W/abstract/'
    band_names = ('sweetspot_dr1_J', 'sweetspot_dr1_H', 'sweetspot_dr1_K')
    zero_point = (25, 25, 25)

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()

        self._photometry_dir = self._data_dir / 'photometry'
        self._table_dir = self._data_dir / 'tables'

        self._photometry_url = 'http://www.phyast.pitt.edu/~wmwv/SweetSpot/DR1_data/lightcurves/'
        self._target_info_url = 'http://www.phyast.pitt.edu/~wmwv/SweetSpot/DR1_data/observed_target_info.dr1.txt'

        self._target_info_path = self._table_dir / 'observed_target_info.dr1.txt'
        self._filter_dir = self._data_dir / 'filters'
        self._filter_zip_path = Path(__file__).parent / 'filters.tar.gz'
        self._filter_file_names = (
            'whirc_J.dat', 'whirc_H.dat', 'whirc_K.dat'
        )

    def _get_available_tables(self) -> List[str]:
        """Get Ids for available vizier tables published by this data release"""

        if self._target_info_path.exists():
            return ['observed_target_info']

        return []

    def _load_table(self, table_id: str) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        if table_id == 'observed_target_info':
            return Table.read(self._target_info_path, format='ascii')

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        obj_ids = set()
        for file in self._photometry_dir.glob('*.Wstd.dat'):
            obj_ids.add(file.stem.split('_')[0])

        return sorted(obj_ids)

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        names = ['Observation', 'MJD', 'Passband', 'Flux', 'Fluxerr-', 'Fluxerr+']
        path = self._photometry_dir / f'{obj_id}_{obj_id}.Wstd.dat'
        table = Table.read(path, format='ascii', names=names)

        if format_table:
            table['time'] = utils.convert_to_jd(table['MJD'])
            table['fluxerr'] = (table['Fluxerr-'] + table['Fluxerr+']) / 2
            table['zp'] = 25
            table['zpsys'] = 'AB'

            table.rename_column('Passband', 'band')
            table.rename_column('Flux', 'flux')
            table.remove_columns(['Fluxerr-', 'Fluxerr+', 'MJD', 'Observation'])

        obs_info = self.load_table('observed_target_info')
        obj_meta = obs_info[obs_info['Name'] == obj_id]

        table.meta.pop('comments')
        table.meta['obj_id'] = obj_id
        table.meta['ra'] = obj_meta['RA']
        table.meta['dec'] = obj_meta['Dec']
        table.meta['z'] = obj_meta['z']
        table.meta['z_err'] = None
        table.meta['n_J'] = obj_meta['n_J']
        table.meta['n_H'] = obj_meta['n_H']
        table.meta['n_K'] = obj_meta['n_K']
        table.meta['Host_J'] = obj_meta['Host_J']
        table.meta['Host_H'] = obj_meta['Host_H']
        table.meta['Host_K'] = obj_meta['Host_K']
        table.meta['notes'] = obj_meta['comments']

        return table

    def _decompress_filters(self):
        """Decompress filter files into the filter directory"""

        print(self._filter_zip_path)
        with tarfile.open(self._filter_zip_path) as data_archive:
            for ffile in data_archive:
                path = self._filter_dir / ffile.name
                if path.exists():
                    continue

                print(f'Unzipping {ffile.name}')

                try:
                    data_archive.extract(ffile, path=self._filter_dir)

                except IOError:
                    path.unlink()
                    data_archive.extract(ffile, path=self._filter_dir)

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        utils.download_file(
            url=self._target_info_url,
            path=self._target_info_path,
            force=force,
            timeout=timeout
        )

        for file_name in _dr1_files:
            file_url = self._photometry_url + file_name

            utils.download_file(
                url=file_url,
                path=self._photometry_dir / file_name,
                force=force,
                timeout=timeout,
                verbose=False
            )

        self._decompress_filters()
