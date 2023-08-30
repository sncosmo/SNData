"""Tests for the ``des.SN3YR`` class."""

from unittest import TestCase, SkipTest

from sndata.des import SN3YR
from ..common_tests import PhotometricDataParsing, PhotometricDataUI

try:
    SN3YR().download_module_data()

except ConnectionError:
    raise SkipTest('Could not connect to one or more remote servers.')


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
