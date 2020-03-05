#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``des`` module."""

from unittest import TestCase

from sndata import des
from .data_parsing_template_tests import PhotometricDataParsing
from .standard_ui_template_tests import PhotometricDataUI


class SN3YRParsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the SN3YR release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = des.SN3YR()
        cls.test_class.download_module_data()


class SN3YRUI(TestCase, PhotometricDataUI):
    """UI tests for the SN3YR release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = des.SN3YR()
