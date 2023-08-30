"""Tests for the ``sweetspot.DR1`` class."""

from unittest import TestCase

from sndata.sweetspot import DR1
from ..common_tests import PhotometricDataParsing, PhotometricDataUI, download_data_or_skip

download_data_or_skip(DR1())


class DR1Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the DR1 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = DR1()

    def test_has_33_objids(self):
        """Test the data release includes all 33 objects"""

        self.assertEqual(33, len(self.test_class.get_available_ids()))


class DR1UI(TestCase, PhotometricDataUI):
    """UI tests for the DR1 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = DR1()
