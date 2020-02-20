#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``sdss`` module"""

from unittest import TestCase

from sndata import sdss
from . import template_tests


class Sako18(TestCase, template_tests.PhotometricDataParsing):
    """Generic tests for a given survey"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = sdss.Sako18()
        cls.test_class.download_module_data()


class Sako18Spec(TestCase, template_tests.SpectroscopicDataParsing):
    """Generic tests for a given survey"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = sdss.Sako18Spec()
        cls.test_class.download_module_data()
