"""Tests for the ``base_classes.PhotometricRelease`` class."""

from unittest import TestCase

from sndata.base_classes import PhotometricRelease
from sndata.exceptions import NoDownloadedData


class PhotometricDataUI(TestCase):
    """Generic UI tests for photometric data releases"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = PhotometricRelease('dummy_survey', 'dummy_release')

    def test_get_data_for_id_no_downloaded_data(self):
        """Test ``get_data_for_id`` raises NoDownloadedData error"""

        self.assertRaises(
            NoDownloadedData, self.test_class.get_data_for_id, 'dummy_id')

    def test_iter_data_no_downloaded_data(self):
        """Test ``iter_data`` raises NoDownloadedData error"""

        with self.assertRaises(NoDownloadedData):
            next(self.test_class.iter_data())

    def test_get_available_tables_no_downloaded_data(self):
        """Test ``get_available_tables`` raises NoDownloadedData error"""

        self.assertRaises(NoDownloadedData, self.test_class.get_available_tables)

    def test_load_table_no_downloaded_data(self):
        """Test ``load_table`` raises NoDownloadedData error"""

        self.assertRaises(NoDownloadedData, self.test_class.load_table, 'dummy_id')

    def test_register_filters_no_downloaded_data(self):
        """Test ``register_filters`` raises NoDownloadedData error"""

        self.assertRaises(NoDownloadedData, self.test_class.register_filters)
