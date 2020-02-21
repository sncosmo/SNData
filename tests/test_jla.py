#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``jla`` module"""

from unittest import TestCase

from sndata import jla
from . import template_tests


class Betoule14(TestCase, template_tests.PhotometricDataParsing):
    """Generic tests for a given survey"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = jla.Betoule14()
        cls.test_class.download_module_data()
