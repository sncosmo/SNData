#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test that survey data is accessed and served correctly"""

from unittest import TestCase

from sndata import csp, des, essence, sdss


class GeneralTests(TestCase):
    """Generic tests for a given survey"""

    def _test_empty_data(self, lim=float('inf')):
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

    def _test_table_parsing(self):
        """Test no errors are raised by ``load_table`` when parsing args from
        ``get_available_tables``
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


class CSP_DR1(GeneralTests):
    """Tests for the csp.dr1 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr1
        cls.module.download_module_data()

    def test_0_empty_data(self):
        self._test_empty_data(10)

    def test_1_table_parsing(self):
        self._test_table_parsing()

    def test_2_sorted_ids(self):
        self._test_ids_are_sorted()


class CSP_DR3(GeneralTests):
    """Tests for the csp.dr3 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr3
        cls.module.download_module_data()

    def test_0_empty_data(self):
        self._test_empty_data(10)

    def test_1_table_parsing(self):
        self._test_table_parsing()

    def test_2_sorted_ids(self):
        self._test_ids_are_sorted()


class SDSS_Sako18(GeneralTests):
    """Tests for the sdss.sako18 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = sdss.sako18
        cls.module.download_module_data()

    def test_0_empty_data(self):
        self._test_empty_data(10)

    def test_1_table_parsing(self):
        self._test_table_parsing()

    def test_2_sorted_ids(self):
        self._test_ids_are_sorted()


class DES_SN3YR(GeneralTests):
    """Tests for the des.SN3YR module"""

    @classmethod
    def setUpClass(cls):
        cls.module = des.sn3yr
        cls.module.download_module_data()

    def test_0_empty_data(self):
        self._test_empty_data(10)

    def test_1_table_parsing(self):
        self._test_table_parsing()

    def test_2_sorted_ids(self):
        self._test_ids_are_sorted()


class ESSENCE_Narayan16(GeneralTests):
    """Tests for the essence.narayan16 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = essence.narayan16
        cls.module.download_module_data()

    def test_0_empty_data(self):
        self._test_empty_data(10)

    def test_1_table_parsing(self):
        self._test_table_parsing()

    def test_2_sorted_ids(self):
        self._test_ids_are_sorted()
