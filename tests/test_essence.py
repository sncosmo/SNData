#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``essence`` module."""

from unittest import TestCase

from sndata import essence
from .data_parsing_template_tests import PhotometricDataParsing
from .standard_ui_template_tests import PhotometricDataUI


class Narayan16Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Narayan16 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = essence.Narayan16()
        cls.test_class.download_module_data()


class Narayan16UI(TestCase, PhotometricDataUI):
    """UI parsing tests for the Narayan16 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = essence.Narayan16()
