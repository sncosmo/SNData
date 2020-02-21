#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``des`` module."""

from unittest import TestCase

from sndata import des
from . import template_tests


class SN3YR(TestCase, template_tests.PhotometricDataParsing):

    @classmethod
    def setUpClass(cls):
        cls.test_class = des.SN3YR()
        cls.test_class.download_module_data()
