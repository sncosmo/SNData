#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Test that survey data is accessed and served correctly for combined data
sets
"""

from unittest import TestCase

from astropy.table import vstack

from sndata import CombinedDataset
from sndata import csp, des
from sndata._combine_data import _reduce_id_mapping
from .data_parsing_template_tests import PhotometricDataParsing
from .test_exceptions import InvalidTableId


class CombinedDataParsing(TestCase, PhotometricDataParsing):
    """Tests the CombinedDataset class using des.SN3YR and csp.DR3 data"""

    @classmethod
    def setUpClass(cls):
        cls.joined_surveys = (csp.DR3(), des.SN3YR())
        cls.test_class = CombinedDataset(*cls.joined_surveys)
        cls.test_class.download_module_data()

    def test_bad_table_id_err(self):
        """Test an InvalidObjId exception is raised for a made up Id"""

        fake_table_id = ('fake_id', 'fake_release', 'fake_survey')
        self.assertRaises(InvalidTableId, self.test_class.load_table, fake_table_id)

    def test_id_joining(self):
        """Test correct data is returned after joining / separating IDs"""

        # Get data for two individual IDs and manual vstack them to get
        # the combined data
        test_ids = [('2004dt', 'DR3', 'CSP'), ('2004ef', 'DR3', 'CSP')]
        expected_obj0_data = self.test_class.get_data_for_id(test_ids[0], True)
        expected_obj1_data = self.test_class.get_data_for_id(test_ids[1], True)
        expected_return = vstack(
            (expected_obj0_data, expected_obj1_data),
            metadata_conflicts='silent'
        )

        # Join IDs and make sure we get the combined data from get_data_for_id
        # sorted operations are only to make unittest reports neater
        self.test_class.join_ids(*test_ids)
        actual_return = self.test_class.get_data_for_id(test_ids[0], True)
        self.assertListEqual(
            sorted(expected_return.as_array().tolist()),
            sorted(actual_return.as_array().tolist()),
            'Incorrect data for joined IDs.'
        )

        # Check we get the original data after separating ids
        self.test_class.separate_ids(*test_ids[0])
        obj0_data = self.test_class.get_data_for_id(test_ids[0], True)
        obj1_data = self.test_class.get_data_for_id(test_ids[1], True)
        self.assertListEqual(
            sorted(expected_obj0_data.as_array().tolist()),
            sorted(obj0_data.as_array().tolist()),
            'Incorrect data for first ID after joining.'
        )

        self.assertListEqual(
            sorted(expected_obj1_data.as_array().tolist()),
            sorted(obj1_data.as_array().tolist()),
            'Incorrect data for second ID after joining.'
        )

    def test_join_id_string_error(self):
        """Test joining object ids as strings raises an error"""

        with self.assertRaises(TypeError):
            self.test_class.join_ids('dummy_id_1', 'dummy_id_2')

        fake_id_as_tuple = ('dummy_id_1', 'dummy_release', 'dummy_survey')
        with self.assertRaises(TypeError):
            self.test_class.join_ids(fake_id_as_tuple, 'dummy_id_2')


class CombinedDataStringIDs(TestCase):
    """Tests usage of string object IDs with CombinedDataset objects"""

    def test_obj_id_as_str(self):
        """Test returned data is the same for obj_ids as strings and tuples"""

        test_class = CombinedDataset(csp.DR3())
        test_class.download_module_data()

        # Known object_id for csp
        test_id = ('2004dt', 'DR3', 'CSP')
        data_from_tuple_id = test_class.get_data_for_id(test_id)
        data_from_str_id = test_class.get_data_for_id(test_id[0])
        self.assertListEqual(
            sorted(data_from_tuple_id.as_array().tolist()),
            sorted(data_from_str_id.as_array().tolist())
        )

    def test_duplicate_obj_id_strings(self):
        """Test an error is raised for non unique string Ids"""

        dummy_release = csp.DR3()
        dummy_release.release = '234'
        combined_data = CombinedDataset(csp.DR3(), dummy_release)
        with self.assertRaises(RuntimeError):
            combined_data.get_data_for_id('2010ae')


class MapReduction(TestCase):
    """Tests for the _reduce_id_mapping function"""

    def test_empty_sets(self):
        """Test _reduce_id_mapping removes empty sets"""

        map_in = [{1, 2, 3}, {4, 5}, {}]
        expected_map = [{1, 2, 3}, {4, 5}]
        self.assertListEqual(expected_map, _reduce_id_mapping(map_in))

    def test_joining(self):
        """Test _reduce_id_mapping correctly joins sets"""

        map_in = [{1, 2, 3}, {3, 4}, {5, 6}, {6, 7}, {7, 8}]
        expected_map = [{1, 2, 3, 4}, {5, 6, 7, 8}]
        self.assertListEqual(expected_map, _reduce_id_mapping(map_in))

    def test_single_value_sets(self):
        """Test _reduce_id_mapping removes empty of length 1"""

        map_in = [{1, 2, 3}, {4, 5}, {7}]
        expected_map = [{1, 2, 3}, {4, 5}]
        self.assertListEqual(expected_map, _reduce_id_mapping(map_in))
