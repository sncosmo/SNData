#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``snls`` module"""

from unittest import TestCase, skip

from sndata import snls
from . import template_tests


class Balland09(TestCase, template_tests.SpectroscopicDataParsing):
    """Generic tests for a given survey"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = snls.Balland09()
        cls.test_class.download_module_data()

    @skip('Ballan09 data tables do not have dates')
    def test_jd_time_format(self):
        pass
