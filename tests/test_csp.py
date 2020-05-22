#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``csp`` module."""

from unittest import TestCase

import numpy as np

from sndata import csp
from .data_parsing_template_tests import PhotometricDataParsing, SpectroscopicDataParsing
from .standard_ui_template_tests import PhotometricDataUI, SpectroscopicDataUI


class DR1Parsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the DR1 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = csp.DR1()
        cls.test_class.download_module_data()


class DR1UI(TestCase, SpectroscopicDataUI):
    """UI tests for the DR1 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = csp.DR1()


class DR3Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the DR3 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = csp.DR3()
        cls.test_class.download_module_data()

    def test_instrument_offsets_ar_applied(self):
        """Test returned DR3 data includes the instrument offset using a
         single data point from 2005el.
         """

        def get_test_point(band, obj_id='2005el', **kwargs):
            data = csp.DR3().get_data_for_id(obj_id, **kwargs)
            y_data = data[data['band'] == band]
            return y_data[0]

        unformatted_data = get_test_point('Y', '2005el', format_table=False)
        formatted_data = get_test_point('csp_dr3_Y', '2005el')

        # Check magnitude offset from natural to AB mag
        offset = np.round(formatted_data['mag'] - unformatted_data['mag'], 4)
        Yband_offset = 0.63  # From Krisciunas et al. 2017
        self.assertEqual(offset, Yband_offset)

        # Check error in mag is not changed
        self.assertEqual(formatted_data['mag_err'], unformatted_data['mag_err'])


class DR3UI(TestCase, PhotometricDataUI):
    """UI tests for the DR3 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = csp.DR3()
