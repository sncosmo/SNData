#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Tests for the ``csp.dr3`` module."""

import numpy as np

from sndata import csp
from .base_tests import DataParsingTestBase, DocumentationTestBase


class DataParsing(DataParsingTestBase):
    """Tests for the csp.dr3 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr3
        cls.module.download_module_data(force=True)

    def test_get_zp(self):
        self._test_get_zp()

    def test_ids_are_sorted(self):
        self._test_ids_are_sorted()

    def test_instrument_offset(self):
        """Test returned DR3 data encorporates the instrument offset using a
         single data point from 2005el.
         """

        def get_test_point(band, obj_id='2005el', time=2453640.80, **kwargs):
            data = csp.dr3.get_data_for_id(obj_id, **kwargs)
            y_data = data[data['band'] == band]
            return y_data[y_data['time'] == time]

        unformated_data = get_test_point('Y', '2005el', format_table=False)
        formated_data = get_test_point('csp_dr3_Y', '2005el')

        # Check magnitude offset from natural to AB mag
        offset = np.round(formated_data['mag'] - unformated_data['mag'], 4)
        Yband_offset = 0.63  # From Krisciunas et al. 2017
        self.assertEqual(offset, Yband_offset)

        # Check error in mag is not changed
        self.assertEqual(formated_data['mag_err'], unformated_data['mag_err'])

    def test_jd_time_format(self):
        self._test_jd_time_format('time')

    def test_no_empty_data_tables(self):
        self._test_no_empty_data_tables(10)

    def test_paper_tables_are_parsed(self):
        self._test_paper_tables_are_parsed()

    def test_sncosmo_column_names(self):
        self._test_sncosmo_column_names()

    def test_sncosmo_registered_band_names(self):
        self._test_sncosmo_registered_band_names()

    def test_unique_ids(self):
        self._test_unique_ids()


class Documentation(DocumentationTestBase):
    """Tests for the des.SN3YR module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr3

    def test_ads_url(self):
        self._test_ads_url_status()

    def test_consistent_docs(self):
        self._test_consistent_docs()

    def test_has_meta_attributes(self):
        self._test_has_meta_attributes()

    def test_survey_url(self):
        self._test_survey_url_status()
