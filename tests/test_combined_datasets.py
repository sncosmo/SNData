#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test that survey data is accessed and served correctly for combined data
sets
"""

from unittest import TestCase

from astropy.table import vstack

from sndata import csp, des
from sndata._combine_data import CombinedDataset, _reduce_id_mapping
from .test_surveys_data import GeneralTests


class Combined(GeneralTests):
    """Tests the CombinedDataset class using des.sn3yr and csp.dr3 data"""

    @classmethod
    def setUpClass(cls):
        cls.joined_surveys = (csp.dr3, des.sn3yr)
        cls.module = CombinedDataset(*cls.joined_surveys)
        cls.module.download_module_data()

    def test_obj_id_dataframe(self):
        """Test for expected data releases in object id DataFrame"""

        expected = set(s.survey_abbrev.lower() for s in self.joined_surveys)
        actual = set(self.module._obj_ids['survey'])
        self.assertEqual(expected, actual)

    def test_id_joining(self):
        """Test correct data is returned after joining / separating IDs"""

        # Get data for two individual IDs and manual vstack them to get
        # the combined data
        test_ids = [('2004dt', 'dr3', 'csp'), ('2004ef', 'dr3', 'csp')]
        expected_obj0_data = self.module.get_data_for_id(test_ids[0], True)
        expected_obj1_data = self.module.get_data_for_id(test_ids[1], True)
        expected_return = vstack(
            (expected_obj0_data, expected_obj1_data),
            metadata_conflicts='silent')

        # Join IDs and make sure we get the combined data from get_data_for_id
        # sorted operations are only to make unittest reports neater
        self.module.join_ids(*test_ids)
        actual_return = self.module.get_data_for_id(test_ids[0], True)
        self.assertListEqual(
            sorted(expected_return.as_array().tolist()),
            sorted(actual_return.as_array().tolist()),
            'Incorrect data for joined IDs.'
        )

        # Check we get the original data after seperating ids
        self.module.separate_ids(test_ids[0])
        obj0_data = self.module.get_data_for_id(test_ids[0], True)
        obj1_data = self.module.get_data_for_id(test_ids[1], True)
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

    def test_ids_are_sorted(self):
        self._test_ids_are_sorted()

    def test_empty_data(self):
        self._test_empty_data(10)


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
