#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides template testing classes for the user interface of
spectroscopic and photometric data releases.
"""

import os
from tempfile import TemporaryDirectory

from sndata.exceptions import InvalidObjId, InvalidTableId
from sndata.exceptions import NoDownloadedData


class SimulateNoDownloadedData:
    """Context manager for simulating do downloaded data

    Example:
        from sndata.csp import DR3

        # This is the instance we wish to test
        dr3 = DR3()

        # test_instance is an instance of dr3 with no downloaded data
        with SimulateNoDownloadedData(dr3) as test_instance:
            # write some tests here
            pass
    """

    def __init__(self, test_class=None):
        self._old_dir = None
        self._temp_dir = None
        self._sndata_dir_name = 'SNDATA_DIR'
        self.test_class = test_class

    def __enter__(self):
        self._old_dir = os.environ.get(self._sndata_dir_name, None)
        self._temp_dir = TemporaryDirectory()
        os.environ[self._sndata_dir_name] = self._temp_dir.name
        if self.test_class:
            return type(self.test_class)()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._old_dir is None:
            os.environ.pop(self._sndata_dir_name)

        else:
            os.environ[self._sndata_dir_name] = self._old_dir

        self._temp_dir.cleanup()


class VizierTableUI:
    """Generic UI tests for vizier table data releases"""

    def test_bad_table_id_err(self):
        """Test an InvalidObjId exception is raised for a made up Id"""

        self.assertRaises(InvalidTableId, self.test_class.load_table, 'fake_id')

    def test_get_available_tables_no_downloaded_data(self):
        """Test ``get_available_tables`` raises NoDownloadedData error"""

        with SimulateNoDownloadedData(self.test_class) as dummy_class:
            self.assertRaises(NoDownloadedData, dummy_class.get_available_tables)

    def test_load_table_no_downloaded_data(self):
        """Test ``load_table`` raises NoDownloadedData error"""

        valid_table_number = self.test_class.get_available_tables()[0]
        with SimulateNoDownloadedData(self.test_class) as dummy_class:
            self.assertRaises(
                NoDownloadedData, dummy_class.load_table, valid_table_number)


class SpectroscopicDataUI(VizierTableUI):
    """Generic UI tests for spectroscopic data releases"""

    def test_bad_object_id_err(self):
        """Test an InvalidObjId exception is raised for a made up Id"""

        self.assertRaises(InvalidObjId, self.test_class.get_data_for_id, 'fake_id')

    def test_not_missing_metadata(self):
        """Test that standard metadata attributes are not null"""

        test_attrs = [
            'survey_name',
            'survey_abbrev',
            'release',
            'survey_url',
            'publications'
        ]

        msg = '``{}`` attribute is not set'
        for attr in test_attrs:
            attr_value = getattr(self.test_class, attr)
            self.assertIsNotNone(attr_value, msg.format(attr))

        self.assertTrue(self.test_class.publications, msg.format('publications'))

    def test_correct_data_type_attribute(self):
        """Test the ``data_type`` attribute is set to ``spectroscopic``"""

        self.assertEqual(self.test_class.data_type, 'spectroscopic')

    def test_get_available_ids_no_downloaded_data(self):
        """Test ``get_available_ids`` raises NoDownloadedData error"""

        with SimulateNoDownloadedData(self.test_class) as dummy_class:
            self.assertRaises(NoDownloadedData, dummy_class.get_available_ids)

    def test_get_data_for_id_no_downloaded_data(self):
        """Test ``get_data_for_id`` raises NoDownloadedData error"""

        valid_obj_id = self.test_class.get_available_ids()[0]
        with SimulateNoDownloadedData(self.test_class) as dummy_class:
            self.assertRaises(
                NoDownloadedData, dummy_class.get_data_for_id, valid_obj_id)

    def test_iter_data_no_downloaded_data(self):
        """Test ``iter_data`` raises NoDownloadedData error"""

        with SimulateNoDownloadedData(self.test_class) as dummy_class:
            with self.assertRaises(NoDownloadedData):
                next(dummy_class.iter_data())


class PhotometricDataUI(SpectroscopicDataUI):
    """Generic UI tests for photometric data releases"""

    def test_not_missing_metadata(self):
        """Test that standard metadata attributes are not null"""

        super().test_not_missing_metadata()

        test_attrs = [
            'band_names',
            'zero_point'
        ]

        msg = '``{}`` attribute is not set'
        for attr in test_attrs:
            attr_value = getattr(self.test_class, attr)
            self.assertTrue(attr_value, msg.format(attr))

    def test_correct_data_type_attribute(self):
        """Test the ``data_type`` attribute is set to ``spectroscopic``"""

        self.assertEqual(self.test_class.data_type, 'photometric')

    def test_register_filters_no_downloaded_data(self):
        """Test ``register_filters`` raises NoDownloadedData error"""

        with SimulateNoDownloadedData(self.test_class) as dummy_class:
            self.assertRaises(NoDownloadedData, dummy_class.register_filters)
