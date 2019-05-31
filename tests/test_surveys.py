#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test input data used for fitting light-curves with SNCosmo."""

from unittest import TestCase

from SNData import csp, sdss


class GeneralTests(TestCase):
    """Generic tests for a given survey"""

    def _test_empty_data(self):
        """Test for empty tables in ``iter_data``"""

        for input_table in self.module.iter_data():
            obj_id = input_table.meta['obj_id']
            self.assertTrue(
                input_table,
                msg=f'Empty table for obj_id {obj_id}.')

    def _test_delete_data(self):
        """Test ``delete_module_data`` agrees with ``data_is_available``"""

        if not self.module.data_is_available():
            err_msg = f'No data found. Cannot test deletion.'
            raise RuntimeError(err_msg)

        self.module.delete_module_data()
        self.assertFalse(self.module.data_is_available())

    def _test_table_parsing(self):
        """Test no errors are raised by ``load_table`` when parsing args from
        ``get_available_tables``
        """

        table_nums = self.module.get_available_tables()
        self.assertGreater(
            len(table_nums), 0, f'No tables available for survey')

        err_msg = 'Empty table number {}'
        for n in table_nums:
            try:
                table = self.module.load_table(n)

            except:
                raise RuntimeError(f'Cannot parse table {n}')

            self.assertTrue(table, err_msg.format(n))


class CSP_DR1(GeneralTests):
    """Tests for the csp.dr1 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr1
        cls.module.download_module_data()

    def test_0_empty_data(self):
        self._test_empty_data()

    def test_1_table_parsing(self):
        self._test_table_parsing()

    def test_2_delete_data(self):
        self._test_delete_data()


class CSP_DR3(GeneralTests):
    """Tests for the csp.dr3 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr3
        cls.module.download_module_data()

    def test_0_empty_data(self):
        self._test_empty_data()

    def test_1_table_parsing(self):
        self._test_table_parsing()

    def test_2_delete_data(self):
        self._test_delete_data()


class SDSS_SAKO14(GeneralTests):
    """Tests for the sdss.sako14 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = sdss.sako14
        cls.module.download_module_data()

    def test_0_empty_data(self):
        self._test_empty_data()

    def test_1_table_parsing(self):
        self._test_table_parsing()

    def test_2_delete_data(self):
        self._test_delete_data()
