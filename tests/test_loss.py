#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``loss`` module."""

from unittest import TestCase

from sndata import loss
from .data_parsing_template_tests import PhotometricDataParsing
from .standard_ui_template_tests import PhotometricDataUI


class Stahl19Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Stahl19 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = loss.Stahl19()
        cls.test_class.download_module_data()


class Stahl19UI(TestCase, PhotometricDataUI):
    """UI tests for the Stahl19 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = loss.Stahl19()


class Ganeshalingam13Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Ganeshalingam13 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = loss.Ganeshalingam13()
        cls.test_class.download_module_data()


class Ganeshalingam13UI(TestCase, PhotometricDataUI):
    """UI tests for the Ganeshalingam13 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = loss.Ganeshalingam13()
