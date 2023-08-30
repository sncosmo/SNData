"""Tests for the ``sdss.Sako18`` class"""

from unittest import TestCase

from sndata.sdss import Sako18
from ..common_tests import PhotometricDataParsing, PhotometricDataUI, download_data_or_skip

download_data_or_skip(Sako18())


class Sako18Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Sako18 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Sako18()


class Sako18UI(TestCase, PhotometricDataUI):
    """UI tests for the Sako18 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Sako18()
