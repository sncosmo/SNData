#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides template testing classes for spectroscopic and
photometric data parsing.
"""

import numpy as np
import sncosmo

from sndata import get_zp
from sndata.exceptions import InvalidTableId


class SpectroscopicDataParsing:
    """Generic data parsing tests for spectroscopic data releases"""

    date_col_name = 'time'  # Name of column to check for JD time format

    def test_no_empty_data_tables(self, lim: int = 25):
        """Test for empty tables in ``iter_data``

        Args:
            lim: Maximum number of tables to check (default: 25)
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

    def test_unique_ids(self):
        """Test all object Ids are unique"""

        obj_ids = self.test_class.get_available_ids()
        unique_elements, count = np.unique(obj_ids, return_counts=True, axis=0)
        duplicates = unique_elements[count > 1]
        self.assertTrue(len(duplicates) == 0, f'Duplicate Ids: {duplicates}')

    def test_no_empty_ids(self):
        """Test no object Ids are empty strings"""

        self.assertNotIn('', self.test_class.get_available_ids())

    def test_cache_not_mutated(self):
        """Test mutating returned tables does not mutate them in the cache"""

        table_names = self.test_class.get_available_tables()
        if len(table_names) == 0:
            self.fail('No available Tables')

        table_id = table_names[0]
        original_table = self.test_class.load_table(table_id)
        original_table_len = len(original_table)
        original_table.remove_row(0)
        new_table = self.test_class.load_table(table_id)

        self.assertEqual(
            original_table_len, len(new_table),
            'Table length was mutated in memory')

    def test_ids_are_sorted(self):
        """Test ``get_available_ids`` returns sorted ids"""

        obj_ids = self.test_class.get_available_ids()
        is_sorted = all(
            obj_ids[i] <= obj_ids[i + 1] for i in range(len(obj_ids) - 1))

        self.assertTrue(is_sorted)

    def test_jd_time_format(self):
        """Test time values are specified as julian dates when formatting
        for sncosmo.
        """

        col_name = self.date_col_name
        test_id = self.test_class.get_available_ids()[0]
        test_data = self.test_class.get_data_for_id(test_id, format_table=True)
        is_greater = np.greater(test_data[col_name], 275300.5).all()
        self.assertTrue(is_greater)

    def test_metadata_order(self):
        """Test data table metadata has the expected minimum data"""

        test_id = self.test_class.get_available_ids()[0]
        test_data = self.test_class.get_data_for_id(test_id)
        ordered_meta_keys = list(test_data.meta.keys())
        expected_order = ['obj_id', 'ra', 'dec', 'z', 'z_err']
        self.assertSequenceEqual(expected_order, ordered_meta_keys[:5])

    def test_comments_not_in_metadata(self):
        """Test there is no 'comments' key in the  data table metadata"""

        test_id = self.test_class.get_available_ids()[0]
        test_data = self.test_class.get_data_for_id(test_id)
        self.assertNotIn('comments', test_data.meta)

    def test_bad_table_id_err(self):
        """Test an InvalidObjId exception is raised for a made up Id"""

        self.assertRaises(InvalidTableId, self.test_class.load_table, 'fake_id')

    def test_paper_tables_are_parsed(self):
        """Test no errors are raised by ``load_table`` when parsing any of the
        table numbers returned by ``get_available_tables``
        """

        table_names = self.test_class.get_available_tables()
        if len(table_names) == 0:
            self.fail('No available Tables')

        err_msg = 'Empty table number {}'
        for table in table_names:
            try:
                table = self.test_class.load_table(table)

            except:
                self.fail(f'Cannot parse table {table}')

            self.assertTrue(table, err_msg.format(table))

    def test_column_names(self):
        """Test columns required by sncosmo are included in formatted tables

        Columns checked to exist include:
            'time', 'band', 'flux'
        """

        test_id = self.test_class.get_available_ids()[0]
        test_data = self.test_class.get_data_for_id(test_id, format_table=True)

        expected_cols = ('time', 'wavelength', 'flux')
        for column in expected_cols:
            self.assertIn(column, test_data.colnames)


class PhotometricDataParsing(SpectroscopicDataParsing):
    """Generic data parsing tests for photometric data releases"""

    def test_get_zp(self):
        """Test that ``sndata.get_zp`` returns the correct zero point"""

        returned_zp = [get_zp(b) for b in self.test_class.band_names]
        actual_zp = self.test_class.zero_point
        self.assertSequenceEqual(actual_zp, returned_zp)

    def test_column_names(self):
        """Test columns required by sncosmo are included in formatted tables

        Columns checked to exist include:
            'time', 'band', 'flux', 'fluxerr', 'zp', 'zpsys'
        """

        test_id = self.test_class.get_available_ids()[0]
        test_data = self.test_class.get_data_for_id(test_id, format_table=True)

        expected_cols = ('time', 'band', 'flux', 'fluxerr', 'zp', 'zpsys')
        for column in expected_cols:
            self.assertIn(column, test_data.colnames)

    def test_sncosmo_registered_band_names(self):
        """Test registered bands do have the correct name"""

        self.test_class.register_filters(force=True)
        for band_name in self.test_class.band_names:
            sncosmo_band = sncosmo.get_bandpass(band_name)
            self.assertEqual(band_name, sncosmo_band.name)
