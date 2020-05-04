#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``bsnip`` module."""

from unittest import TestCase

from sndata import bsnip
from .data_parsing_template_tests import SpectroscopicDataParsing
from .standard_ui_template_tests import SpectroscopicDataUI


class Silverman12Parsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the Silverman12 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = bsnip.Silverman12()
        cls.test_class.download_module_data()


class Silverman12UI(TestCase, SpectroscopicDataUI):
    """UI tests for the Silverman12 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = bsnip.Silverman12()


class Stahl20Parsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the Stahl20 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = bsnip.Stahl20()
        cls.test_class.download_module_data()


class Stahl20UI(TestCase, SpectroscopicDataUI):
    """UI tests for the Stahl20 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = bsnip.Stahl20()
