#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``sweetspot`` module."""

from unittest import TestCase

from sndata import sweetspot
from .data_parsing_template_tests import PhotometricDataParsing
from .standard_ui_template_tests import PhotometricDataUI


class DR1Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the DR1 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = sweetspot.DR1()
        cls.test_class.download_module_data()

    def test_has_33_objids(self):
        """Test the data release includes all 33 objects"""

        self.assertEqual(33, len(self.test_class.get_available_ids()))


class DR1UI(TestCase, PhotometricDataUI):
    """UI tests for the DR1 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = sweetspot.DR1()
