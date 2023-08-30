"""Tests for the ``essence.Narayan16`` class."""

from unittest import TestCase

from sndata.essence import Narayan16
from ..common_tests import PhotometricDataParsing, PhotometricDataUI, download_data_or_skip

download_data_or_skip(Narayan16())


class Narayan16Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Narayan16 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Narayan16()


class Narayan16UI(TestCase, PhotometricDataUI):
    """UI parsing tests for the Narayan16 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Narayan16()
