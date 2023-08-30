"""Tests for the ``csp.DR1`` class."""

from unittest import TestCase

from sndata.csp import DR1
from ..common_tests import SpectroscopicDataParsing, SpectroscopicDataUI, download_data_or_skip

download_data_or_skip(DR1())


class DR1Parsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the DR1 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = DR1()


class DR1UI(TestCase, SpectroscopicDataUI):
    """UI tests for the DR1 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = DR1()
