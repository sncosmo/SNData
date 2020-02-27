#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``jla`` module"""

from unittest import TestCase

from sndata import jla
from .data_parsing_template_tests import PhotometricDataParsing
from .standard_ui_template_tests import PhotometricDataUI


class Betoule14Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Betoule14 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = jla.Betoule14()
        cls.test_class.download_module_data()


class Betoule14UI(TestCase, PhotometricDataUI):
    """UI tests for the Betoule14 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = jla.Betoule14()
        cls.test_class.download_module_data()
