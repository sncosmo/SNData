"""Tests for the ``jla.Betoule14`` class"""

from unittest import TestCase

from sndata.jla import Betoule14
from ..common_tests import PhotometricDataParsing, PhotometricDataUI, download_data_or_skip

download_data_or_skip(Betoule14())


class Betoule14Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Betoule14 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Betoule14()


class Betoule14UI(TestCase, PhotometricDataUI):
    """UI tests for the Betoule14 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Betoule14()
