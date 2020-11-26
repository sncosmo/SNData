#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the CSP DR1 API"""

from pathlib import Path
from typing import List

from astropy.table import Table, vstack

from ..base_classes import DefaultParser, SpectroscopicRelease
from ..utils import downloads, data_parsing


class DR1(DefaultParser, SpectroscopicRelease):
    """The ``DR1`` class provides access to spectra from the first release of
    optical spectroscopic data of low-redshift Type Ia supernovae (SNe Ia) by
    the Carnegie Supernova Project. It includes 604 previously unpublished
    spectra of 93 SNe Ia. The observations cover a range of phases from 12 days
    before to over 150 days after the time of B-band maximum light.
    (Source: Folatelli et al. 2013)

    .. important:: The DR1 spectra are both published and returned by sndata
       in units of rest frame wavelength.

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    # General metadata
    survey_name = 'Carnegie Supernova Project'
    release = 'DR1'
    survey_abbrev = 'CSP'
    survey_url = 'https://csp.obs.carnegiescience.edu/news-items/CSP_spectra_DR1'
    publications = ('Folatelli et al. 2013',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2013ApJ...773...53F/abstract'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()

        # Local paths
        self._spectra_dir = self._data_dir / 'CSP_spectra_DR1'
        self._table_dir = self._data_dir / 'tables'

        # Define urls for remote data
        self._spectra_url = 'https://csp.obs.carnegiescience.edu/data/CSP_spectra_DR1.tgz'
        self._table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/ApJ/773/53'

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        files = self._spectra_dir.glob('SN*.dat')
        ids = ('20' + Path(f).name.split('_')[0].lstrip('SN') for f in files)
        return sorted(set(ids))

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        files = self._spectra_dir.rglob(f'SN{obj_id[2:]}_*.dat')
        if not files:
            raise ValueError(f'No data found for obj_id {obj_id}')

        return vstack([data_parsing.read_csp_spectroscopy_file(path, format_table) for path in files])

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        downloads.download_tar(
            url=self._table_url,
            out_dir=self._table_dir,
            skip_exists=self._table_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )

        # Download spectra
        downloads.download_tar(
            url=self._spectra_url,
            out_dir=self._data_dir,
            skip_exists=self._spectra_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )
