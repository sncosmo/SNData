#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the Essence Narayan16 API"""

from pathlib import Path
from typing import List

import numpy as np
from astropy.table import Table

from .. import utils
from ..base_classes import DefaultParser, PhotometricRelease
from ..exceptions import InvalidObjId


def _format_table(data_table: Table) -> Table:
    """Format a data table for use with SNCosmo

    Args:
        data_table: A data table returned by ``get_data_for_id``

    Returns:
        The same data in a new table following the SNCosmo data model
    """

    out_table = Table()
    out_table.meta = data_table.meta

    out_table['time'] = utils.convert_to_jd(data_table['MJD'])
    out_table['band'] = ['csp_dr3_' + band for band in data_table['Passband']]
    out_table['zp'] = np.full(len(data_table), 25)
    out_table['zpsys'] = np.full(len(data_table), 'ab')
    out_table['flux'] = data_table['Flux']
    out_table['fluxerr'] = np.max(
        [data_table['Fluxerr_hi'], data_table['Fluxerr_lo']], axis=0)

    return out_table


class Narayan16(PhotometricRelease, DefaultParser):
    """The ``Narayan16`` class provides access to photometric data for 213
    Type Ia supernovae discovered by the ESSENCE survey at redshifts
    0.1 <= z <= 0.81 between 2002 and 2008. It includes R and I band photometry
    measured from images obtained using the MOSAIC II camera at the CTIO
    Blanco telescope. (Source: Narayan et al. 2016)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    # General metadata
    survey_name = 'Equation of State: Supernovae trace Cosmic Expansion'
    survey_abbrev = 'ESSENCE'
    release = 'Narayan16'
    survey_url = 'http://www.ctio.noao.edu/essence/'
    publications = ('Narayan et al. 2016',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2016ApJS..224....3N/abstract'

    # Photometric metadata (Required for photometric data, otherwise delete)
    band_names = ('essence_narayan16_R', 'essence_narayan16_I')
    zero_point = (27.5, 27.5)

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()

        # Local paths
        self._table_dir = self._data_dir / 'vizier'
        self._photometry_dir = self._table_dir / 'lcs'
        self._filter_dir = self._data_dir / 'filters'

        # Define urls for remote data
        self._table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/ApJS/224/3'
        self._filter_urls = (
            'https://www.noao.edu/kpno/mosaic/filters/asc6004.f287.r04.txt',
            'https://www.noao.edu/kpno/mosaic/filters/asc6028.f287.r04.txt'
        )

        self._filter_file_names = ('R_band.dat', 'I_band.dat')

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        files = self._photometry_dir.glob('*.dat')
        return sorted(Path(f).name.split('.')[0] for f in files)

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

        # Get photometric data
        path = self._photometry_dir / f'{obj_id}.W6yr.clean.nn2.Wstd.dat'
        data_table = Table.read(
            path, format='ascii',
            names=['Observation', 'MJD', 'Passband', 'Flux', 'Fluxerr_lo', 'Fluxerr_hi']
        )

        # Get meta data
        table_6 = self.load_table(6)
        object_metadata = table_6[table_6['ESSENCE'] == obj_id][0]
        ra, dec = utils.hourangle_to_degrees(
            rah=object_metadata['RAh'],
            ram=object_metadata['RAm'],
            ras=object_metadata['RAs'],
            dec_sign=object_metadata['DE-'],
            decd=object_metadata['DEd'],
            decm=object_metadata['DEm'],
            decs=object_metadata['DEs']
        )

        data_table.meta['obj_id'] = obj_id
        data_table.meta['ra'] = ra
        data_table.meta['dec'] = dec
        data_table.meta['z'] = object_metadata['zSNID']
        data_table.meta['z_err'] = object_metadata['e_zSNID']
        del data_table.meta['comments']

        if format_table:
            data_table = _format_table(data_table)

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

        for filter_file, filter_url in zip(self._filter_file_names, self._filter_urls):
            utils.download_file(
                url=filter_url,
                path=self._filter_dir / filter_file,
                force=force,
                timeout=timeout
            )
