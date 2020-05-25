#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``osc`` module."""

from unittest import TestCase

from sndata import osc
from .data_parsing_template_tests import PhotometricDataParsing, SpectroscopicDataParsing
from .standard_ui_template_tests import PhotometricDataUI, SpectroscopicDataUI


class OSCPhotParsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the OSCPhot release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = osc.OSCPhot()
        cls.test_class._download_module_data()


class OSCPhotUI(TestCase, PhotometricDataUI):
    """UI tests for the OSCPhot release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = osc.OSCPhot()
        cls.test_class._download_module_data()


class OSCSpecParsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the OSCPhot release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = osc.OSCSpec()
        cls.test_class._download_module_data()


class OSCSpecUI(TestCase, SpectroscopicDataUI):
    """UI tests for the OSCPhot release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = osc.OSCSpec()
        cls.test_class._download_module_data()
