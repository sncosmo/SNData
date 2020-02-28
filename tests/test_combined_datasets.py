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


class Combined(TestCase, PhotometricDataParsing):
    """Tests the CombinedDataset class using des.sn3yr and csp.dr3 data"""

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

        # Check we get the original data after seperating ids
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
