#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``snls`` module"""

from unittest import TestCase
from unittest import skip

from sndata import snls
from .data_parsing_template_tests import SpectroscopicDataParsing
from .standard_ui_template_tests import SpectroscopicDataUI


class Balland09Parsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the Balland09 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = snls.Balland09()
        cls.test_class.download_module_data()

    @skip('Balland09 data tables do not have dates')
    def test_jd_time_format(self):
        pass

    def test_column_names(self):
        """Test columns required by sncosmo are included in formatted tables

        Columns checked to exist include:
            'phase', 'band', 'flux'
        """

        test_id = self.test_class.get_available_ids()[0]
        test_data = self.test_class.get_data_for_id(test_id, format_table=True)

        expected_cols = ('phase', 'wavelength', 'flux')
        for column in expected_cols:
            self.assertIn(column, test_data.colnames)


class Balland09UI(TestCase, SpectroscopicDataUI):
    """UI tests for the Balland09 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = snls.Balland09()
