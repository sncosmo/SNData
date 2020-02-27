#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``snls`` module"""

from unittest import TestCase
from unittest import skip

from sndata import snls
from .data_parsing_template_tests import SpectroscopicDataParsing
from .standard_ui_template_tests import SpectroscopicDataUI


class Balland09Parsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the Balland09 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = snls.Balland09()
        cls.test_class.download_module_data()

    @skip('Balland09 data tables do not have dates')
    def test_jd_time_format(self):
        pass


class Balland09UI(TestCase, SpectroscopicDataUI):
    """UI tests for the Balland09 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = snls.Balland09()
