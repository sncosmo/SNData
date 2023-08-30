"""Tests for the ``loss.Ganeshalingam13`` class."""

from unittest import TestCase

from sndata.loss import Ganeshalingam13
from ..common_tests import PhotometricDataParsing, PhotometricDataUI, download_data_or_skip

download_data_or_skip(Ganeshalingam13())


class Ganeshalingam13Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Ganeshalingam13 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Ganeshalingam13()


class Ganeshalingam13UI(TestCase, PhotometricDataUI):
    """UI tests for the Ganeshalingam13 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Ganeshalingam13()
