#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test that survey data is accessed and served correctly for combined data
sets
"""

from unittest import TestCase

from astropy.table import vstack

from SNData import csp, des
from SNData._combine_data import CombinedDataset, _reduce_id_mapping


# Todo: Finish tests for CombinedDataset class
class Combined(TestCase):
    """Tests the CombinedDataset class using des.sn3yr and csp.dr3 data"""

    @classmethod
    def setUpClass(cls):
        cls.module = CombinedDataset(csp.dr3, des.sn3yr)
        cls.module.download_module_data()

    def test_id_joining(self):
        """Test correct data is returned after joining / separating IDs"""

        test_ids = [('csp', 'dr3', '2004dt'), ('csp', 'dr3', '2004ef')]
        obj1_data = self.module.get_data_for_id(test_ids[0], True)
        obj2_data = self.module.get_data_for_id(test_ids[1], True)
        expected_return = vstack(obj1_data, obj2_data)

        self.module.join_ids(*test_ids)
        actual_return = self.module.get_data_for_id(test_ids[0])
        self.assertEqual(expected_return, actual_return)

        self.module.separate_ids(test_ids[1])
        self.assertEqual(self.module.get_data_for_id(test_ids[0]), obj1_data)

    def test_iter_data(self):
        """Test ``iter_data`` correctly slices data by survey / release value
        """

        pass

    def test_duplicate_ids(self):
        """Test ``get_duplicate_ids`` returns the correct values"""

        pass


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
