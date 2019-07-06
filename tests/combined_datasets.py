#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test that survey data is accessed and served correctly for combined data
sets
"""

from unittest import TestCase

from SNData import csp, des
from SNData._combine_data import CombinedDataset, _reduce_id_mapping


# Todo: Test CombinedDataset class
class Combined(TestCase):
    """Tests the combined des.sn3yr and csp.dr3 modules"""

    @classmethod
    def setUpClass(cls):
        cls.module = CombinedDataset(csp.dr3, des.sn3yr)
        cls.module.download_module_data()


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
