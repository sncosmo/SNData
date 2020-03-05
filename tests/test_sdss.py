#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``sdss`` module"""

from unittest import TestCase

from sndata import sdss
from .data_parsing_template_tests import PhotometricDataParsing, SpectroscopicDataParsing
from .standard_ui_template_tests import PhotometricDataUI, SpectroscopicDataUI


class Sako18Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Sako18 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = sdss.Sako18()
        cls.test_class.download_module_data()


class Sako18UI(TestCase, PhotometricDataUI):
    """UI tests for the Sako18 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = sdss.Sako18()


class Sako18SpecParsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the Sako18Spec release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = sdss.Sako18Spec()
        cls.test_class.download_module_data()


class Sako18SpecUI(TestCase, SpectroscopicDataUI):
    """UI tests for the Sako18Spec release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = sdss.Sako18Spec()
