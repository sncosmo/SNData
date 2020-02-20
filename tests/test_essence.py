#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``essence`` module."""

from unittest import TestCase

from sndata import essence
from . import template_tests


class Narayan16(TestCase, template_tests.PhotometricDataParsing):
    """Generic tests for a given survey"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = essence.Narayan16()
        cls.test_class.download_module_data()
