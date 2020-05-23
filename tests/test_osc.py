#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``osc`` module."""

from unittest import TestCase

from sndata import osc
from .data_parsing_template_tests import PhotometricDataParsing
from .standard_ui_template_tests import PhotometricDataUI


class OSCPhotParsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the OSCPhot release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = osc.OSCPhot()


class OSCPhotUI(TestCase, PhotometricDataUI):
    """UI tests for the OSCPhot release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = osc.OSCPhot()
