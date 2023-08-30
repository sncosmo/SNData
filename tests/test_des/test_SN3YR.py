"""Tests for the ``des.SN3YR`` class."""

from unittest import TestCase

from sndata.des import SN3YR
from ..common_tests import PhotometricDataParsing, PhotometricDataUI, download_data_or_skip

download_data_or_skip(SN3YR())


class SN3YRParsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the SN3YR release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = SN3YR()


class SN3YRUI(TestCase, PhotometricDataUI):
    """UI tests for the SN3YR release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = SN3YR()
