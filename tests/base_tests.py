#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides generic tests that are applicable to a variety of
modules.
"""

import re
from pathlib import Path
from unittest import TestCase
from warnings import warn

import numpy as np
import requests
import sncosmo
import yaml

from sndata import get_zp
from sndata.exceptions import InvalidObjId

docs_path = Path(__file__).resolve().parent / 'docs.yml'
with open(docs_path) as ofile:
    try:
        expected_docs = yaml.load(ofile, Loader=yaml.FullLoader)

    except AttributeError:  # Support older yaml versions
        expected_docs = yaml.load(ofile)


class DataParsingTestBase(TestCase):
    """Generic tests for a given survey"""

    module = None

    def _test_bad_object_id_err(self):
        """Test an InvalidObjId excpetion is raised for a made up Id"""

        self.assertRaises(InvalidObjId, self.module.get_data_for_id, 'fake_id')

    def _test_get_zp(self):
        """Test that ``get_zp`` returns the correct zero point"""

        returned_zp = [get_zp(b) for b in self.module.band_names]
        actual_zp = self.module._meta.zero_point
        self.assertSequenceEqual(actual_zp, returned_zp)

    def _test_ids_are_sorted(self):
        """Test ``get_available_ids`` returns sorted ids"""

        obj_ids = self.module.get_available_ids()
        is_sorted = all(
            obj_ids[i] <= obj_ids[i + 1] for i in range(len(obj_ids) - 1))

        self.assertTrue(is_sorted)

    def _test_jd_time_format(self, col_name):
        """Test time values are specified as julian dates when formatting
        for sncosmo.

        Args:
            col_name (str): The name of the table column to test
        """

        test_id = self.module.get_available_ids()[0]
        test_data = self.module.get_data_for_id(test_id, format_table=True)
        is_greater = np.greater(test_data[col_name], 275300.5).all()
        self.assertTrue(is_greater)

    def _test_lambda_effective(self):
        """Test effective wavelengths provided by sndata match sncosmo"""

        self.module.register_filters(force=True)
        module_lambda = self.module.lambda_effective
        sncosmo_lambda = \
            [sncosmo.get_bandpass(b).wave_eff for b in self.module.band_names]

        self.assertSequenceEqual(module_lambda, sncosmo_lambda)

    def _test_no_empty_data_tables(self, lim=float('inf')):
        """Test for empty tables in ``iter_data``

        Args:
            lim (int): Maximum number of tables to check (default: All tables)
        """

        passed_data = False
        for i, input_table in enumerate(self.module.iter_data()):
            if i >= lim:
                return

            passed_data = True
            obj_id = input_table.meta['obj_id']

            self.assertTrue(
                input_table,
                msg=f'Empty table for obj_id {obj_id}.')

        if not passed_data:
            self.fail('No data yielded')

    def _test_paper_tables_are_parsed(self):
        """Test no errors are raised by ``load_table`` when parsing any of the
        table numbers returned by ``get_available_tables``
        """

        table_names = self.module.get_available_tables()
        self.assertGreater(
            len(table_names), 0, f'No tables available for survey')

        err_msg = 'Empty table number {}'
        for table in table_names:
            try:
                table = self.module.load_table(table)

            except:
                self.fail(f'Cannot parse table {table}')

            self.assertTrue(table, err_msg.format(table))

    def _test_sncosmo_column_names(self):
        """Test columns required by sncosmo are included in formatted tables

        Columns checked to exist include:
            'time', 'band', 'flux', 'fluxerr', 'zp', 'zpsys'
        """

        test_id = self.module.get_available_ids()[0]
        test_data = self.module.get_data_for_id(test_id, format_table=True)

        expected_cols = ('time', 'band', 'flux', 'fluxerr', 'zp', 'zpsys')
        for column in expected_cols:
            self.assertIn(column, test_data.colnames)

    def _test_sncosmo_registered_band_names(self):
        """Test registered bands do have the correct name"""

        self.module.register_filters()
        for band_name in self.module.band_names:
            sncosmo_band = sncosmo.get_bandpass(band_name)
            self.assertEqual(band_name, sncosmo_band.name)

    def _test_unique_ids(self):
        """Test all object Ids are unique"""

        obj_ids = self.module.get_available_ids()
        is_unique = len(np.unique(obj_ids)) == len(obj_ids)
        self.assertTrue(is_unique)


class DocumentationTestBase(TestCase):
    """Generic tests for a given survey

    The data access module being tested should be specified as self.module
    """

    module = None

    def _test_ads_url_status(self):
        """Test module.ads_url returns a 200 status code"""

        try:
            stat_code = requests.get(
                self.module.ads_url, timeout=15).status_code

        except TimeoutError:
            stat_code = 0

        if not stat_code == 200:
            warn(f'Error code {stat_code}: {self.module.survey_url}')

    def _test_consistent_docs(self, skip_funcs=()):
        """Test data access functions have consistent documentation

        Args:
            skip_funcs (iter[str]): Function names to skip during testing
        """

        for func_name, doc_string in expected_docs.items():
            if func_name not in skip_funcs:
                # Strip spaces and indentation but not new lines
                module_func = getattr(self.module, func_name)
                func_doc = re.sub("  +", "", module_func.__doc__)
                expected_doc = re.sub("  +", "", doc_string)

                self.assertEqual(
                    func_doc, expected_doc,
                    f'Wrong docstring for ``{func_name}``')

    def _test_survey_url_status(self):
        """Test module.survey_url returns a 200 status code"""

        try:
            stat_code = requests.get(
                self.module.survey_url, timeout=15).status_code

        except TimeoutError:
            stat_code = 0

        if not stat_code == 200:
            warn(f'Error code {stat_code}: {self.module.survey_url}')

    def _test_has_meta_attributes(self):
        """Test the module has the correct attributes for meta data"""

        expected_attributes = (
            'survey_name',
            'survey_abbrev',
            'release',
            'survey_url',
            'data_type',
            'publications',
            'ads_url')

        for attribute in expected_attributes:
            self.assertTrue(
                hasattr(self.module, attribute),
                f'Missing attribute {attribute}')
