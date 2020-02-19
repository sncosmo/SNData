#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides generic tests that are applicable to a variety of
modules.
"""

from unittest import TestCase

import numpy as np
import sncosmo

from sndata import get_zp
from sndata.exceptions import InvalidObjId


class DataParsingTestBase(TestCase):
    """Generic tests for a given survey"""

    test_class = None

    def _test_bad_object_id_err(self):
        """Test an InvalidObjId exception is raised for a made up Id"""

        self.assertRaises(InvalidObjId, self.test_class.get_data_for_id, 'fake_id')

    def _test_get_zp(self):
        """Test that ``get_zp`` returns the correct zero point"""

        returned_zp = [get_zp(b) for b in self.test_class.band_names]
        actual_zp = self.test_class.zero_point
        self.assertSequenceEqual(actual_zp, returned_zp)

    def _test_ids_are_sorted(self):
        """Test ``get_available_ids`` returns sorted ids"""

        obj_ids = self.test_class.get_available_ids()
        is_sorted = all(
            obj_ids[i] <= obj_ids[i + 1] for i in range(len(obj_ids) - 1))

        self.assertTrue(is_sorted)

    def _test_jd_time_format(self, col_name):
        """Test time values are specified as julian dates when formatting
        for sncosmo.

        Args:
            col_name (str): The name of the table column to test
        """

        test_id = self.test_class.get_available_ids()[0]
        test_data = self.test_class.get_data_for_id(test_id, format_table=True)
        is_greater = np.greater(test_data[col_name], 275300.5).all()
        self.assertTrue(is_greater)

    def _test_lambda_effective(self):
        """Test effective wavelengths provided by sndata match sncosmo"""

        self.test_class.register_filters(force=True)
        module_lambda = self.test_class.lambda_effective
        sncosmo_lambda = \
            [sncosmo.get_bandpass(b).wave_eff for b in self.test_class.band_names]

        self.assertSequenceEqual(module_lambda, sncosmo_lambda)

    def _test_no_empty_data_tables(self, lim=float('inf')):
        """Test for empty tables in ``iter_data``

        Args:
            lim (int): Maximum number of tables to check (default: All tables)
        """

        i = -1
        for i, input_table in enumerate(self.test_class.iter_data()):
            if i >= lim:
                return

            obj_id = input_table.meta['obj_id']
            self.assertTrue(
                input_table,
                msg=f'Empty table for obj_id {obj_id}.')

        if i < 0:
            self.fail('No data yielded')

    def _test_paper_tables_are_parsed(self):
        """Test no errors are raised by ``load_table`` when parsing any of the
        table numbers returned by ``get_available_tables``
        """

        table_names = self.test_class.get_available_tables()
        err_msg = 'Empty table number {}'
        for table in table_names:
            try:
                table = self.test_class.load_table(table)

            except:
                self.fail(f'Cannot parse table {table}')

            self.assertTrue(table, err_msg.format(table))

    def _test_sncosmo_column_names(self):
        """Test columns required by sncosmo are included in formatted tables

        Columns checked to exist include:
            'time', 'band', 'flux', 'fluxerr', 'zp', 'zpsys'
        """

        test_id = self.test_class.get_available_ids()[0]
        test_data = self.test_class.get_data_for_id(test_id, format_table=True)

        expected_cols = ('time', 'band', 'flux', 'fluxerr', 'zp', 'zpsys')
        for column in expected_cols:
            self.assertIn(column, test_data.colnames)

    def _test_sncosmo_registered_band_names(self):
        """Test registered bands do have the correct name"""

        self.test_class.register_filters()
        for band_name in self.test_class.band_names:
            sncosmo_band = sncosmo.get_bandpass(band_name)
            self.assertEqual(band_name, sncosmo_band.name)

    def _test_unique_ids(self):
        """Test all object Ids are unique"""

        obj_ids = self.test_class.get_available_ids()
        unique_elements, counts_elements = np.unique(obj_ids, return_counts=True)
        duplicates = unique_elements[counts_elements > 1]
        is_empty = len(duplicates) == 0
        self.assertTrue(is_empty, f'Duplicate Ids: {duplicates}')

    def _test_cache_not_mutated(self):
        """Test mutating returned tables does not mutate them in the cache"""

        table_id = self.test_class.get_available_tables()[0]
        original_table = self.test_class.load_table(table_id)
        original_table_len = len(original_table)
        original_table.remove_row(0)

        new_table = self.test_class.load_table(table_id)

        self.assertEqual(
            original_table_len, len(new_table),
            'Table length was mutated in memory')
