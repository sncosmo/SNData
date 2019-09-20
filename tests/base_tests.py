#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides generic tests that are applicable to a variety of
modules.
"""

from pathlib import Path
from unittest import TestCase
from warnings import warn

import requests
import sncosmo
import yaml

from sndata import get_zp

docs_path = Path(__file__).resolve().parent / 'docs.yml'
with open(docs_path) as ofile:
    try:
        expected_docs = yaml.load(ofile, Loader=yaml.FullLoader)

    except AttributeError:  # Support older yaml versions
        expected_docs = yaml.load(ofile)


class DataParsingTestBase(TestCase):
    """Generic tests for a given survey"""

    module = None

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

    def _test_ids_are_sorted(self):
        """Test ``get_available_ids`` returns sorted ids"""

        obj_ids = self.module.get_available_ids()
        is_sorted = all(
            obj_ids[i] <= obj_ids[i + 1] for i in range(len(obj_ids) - 1))

        self.assertTrue(is_sorted)

    def _test_get_zp(self):
        """Test that ``get_zp`` returns the correct zero point"""

        returned_zp = [get_zp(b) for b in self.module.band_names]
        actual_zp = self.module._meta.zero_point
        self.assertSequenceEqual(actual_zp, returned_zp)

    def _test_lambda_effective(self):

        self.module.register_filters(force=True)
        module_lambda = self.module.lambda_effective
        sncosmo_lambda = [sncosmo.get_bandpass(b).wave_eff for b in
                          self.module.band_names]
        self.assertSequenceEqual(module_lambda, sncosmo_lambda)

    def _test_jd_time_format(self):
        """Test time values are specified as julian dates when formatting
        for sncosmo."""

        test_id = self.module.get_available_ids()[0]
        test_data = self.module.get_data_for_id(test_id, format_table=True)
        self.assertGreater(test_data['time'][0], 275300.5)

    def _test_sncosmo_column_names(self):
        test_id = self.module.get_available_ids()[0]
        test_data = self.module.get_data_for_id(test_id, format_table=True)

        expected_cols = ('time', 'band', 'flux', 'fluxerr', 'zp', 'zpsys')
        for column in expected_cols:
            self.assertIn(column, test_data.colnames)

    def _test_format_sncosmo_raises_err(self):

        self.assertRaises(
            RuntimeError,
            self.module.get_data_for_id,
            obj_id=self.module.get_available_ids()[0],
            format_table=True)

    def _test_sncosmo_registered_band_names(self):
        """Test registered bands do have the correct name"""

        self.module.register_filters()
        for band_name in self.module.band_names:
            sncosmo_band = sncosmo.get_bandpass(band_name)
            self.assertEqual(band_name, sncosmo_band.name)


class DocumentationTestBase(TestCase):
    """Generic tests for a given survey

    The data access module being tested should be specified as self.module
    """

    module = None

    def _test_consistent_docs(self, skip_funcs=()):
        """Test data access functions have consistent documentation

        Args:
            skip_funcs (iter[str]): Function names to skip during testing
        """

        for func_name, doc_string in expected_docs.items():
            if func_name not in skip_funcs:
                module_func = getattr(self.module, func_name)
                self.assertEqual(doc_string, module_func.__doc__,
                                 f'Wrong docstring for ``{func_name}``')

    def _test_ads_url_status(self):
        """Test module.ads_url returns a 200 status code"""

        stat_code = requests.get(self.module.ads_url).status_code
        if not stat_code == 200:
            warn(f'Error code {stat_code}: {self.module.survey_url}')

    def _test_survey_url_status(self):
        """Test module.survey_url returns a 200 status code"""

        stat_code = requests.get(self.module.survey_url).status_code
        if not stat_code == 200:
            warn(f'Error code {stat_code}: {self.module.survey_url}')
