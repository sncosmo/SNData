#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``osc`` module."""

from unittest import TestCase

from sndata import osc
from .data_parsing_template_tests import PhotometricDataParsing, SpectroscopicDataParsing
from .standard_ui_template_tests import PhotometricDataUI, SpectroscopicDataUI


class OSCBaseParsingTests:
    def test_cache_not_mutated(self):
        """Test mutating returned tables does not mutate them in the cache"""

        table_id = 'catalog'
        data_dict = self.test_class.load_table(table_id)
        data_dict['SN2011fe'] = None

        self.assertIsNotNone(
            self.test_class.load_table(table_id)['SN2011fe'],
            'OSC catalog was mutated in memory')


class OSCPhotParsing(TestCase, OSCBaseParsingTests, PhotometricDataParsing):
    """Data parsing tests for the OSCPhot release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = osc.OSCPhot()
        cls.test_class.download_module_data()


class OSCPhotUI(TestCase, PhotometricDataUI):
    """UI tests for the OSCPhot release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = osc.OSCPhot()
        cls.test_class.download_module_data()


class OSCSpecParsing(TestCase, OSCBaseParsingTests, SpectroscopicDataParsing):
    """Data parsing tests for the OSCPhot release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = osc.OSCSpec()
        cls.test_class.download_module_data()


class OSCSpecUI(TestCase, SpectroscopicDataUI):
    """UI tests for the OSCPhot release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = osc.OSCSpec()
        cls.test_class.download_module_data()
