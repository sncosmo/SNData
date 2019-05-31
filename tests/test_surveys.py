#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test input data used for fitting light-curves with SNCosmo."""

from unittest import TestCase

from SNData import csp, sdss


class GeneralTests(TestCase):
    """Generic tests for a given survey"""

    def _test_empty_tables(self, module, name):
        """Test for empty tables in ``iter_data``

        Args:
            module (module): A data access module
            name      (str): Name of ``module`` for error message
        """

        err_msg = 'Empty table for {} obj_id {}.'
        for input_table in module.iter_data():
            obj_id = input_table.meta['obj_id']
            self.assertTrue(
                input_table,
                msg=err_msg.format(name, obj_id))

    def _test_delete_data(self, module, name):
        """Test ``delete_module_data`` agrees with ``data_is_available``

        Args:
            module (module): A data access module
            name      (str): Name of ``module`` for error message
        """

        if not module.data_is_available():
            raise RuntimeError(
                f'No data found for {name}. Cannot test deletion.')

        module.delete_module_data()
        self.assertFalse(module.data_is_available(), f'Test failed for {name}')


class CSP_DR1(GeneralTests):
    """Tests for the csp.dr1 module"""

    @classmethod
    def setUpClass(cls):
        csp.dr1.download_module_data()

    def test_0_empty_tables(self):
        self._test_empty_tables(csp.dr1, 'csp.dr1')

    def test_1_delete_data(self):
        self._test_delete_data(csp.dr1, 'csp.dr1')


class CSP_DR3(GeneralTests):
    """Tests for the csp.dr3 module"""

    @classmethod
    def setUpClass(cls):
        csp.dr3.download_module_data()

    def test_0_empty_tables(self):
        self._test_empty_tables(csp.dr3, 'csp.dr3')

    def test_1_delete_data(self):
        self._test_delete_data(csp.dr3, 'csp.dr3')


class SDSS_SAKO14(GeneralTests):
    """Tests for the sdss.sako14 module"""

    @classmethod
    def setUpClass(cls):
        sdss.sako14.download_module_data()

    def test_0_empty_tables(self):
        self._test_empty_tables(sdss.sako14, 'sdss.sako14')

    def test_1_delete_data(self):
        self._test_delete_data(sdss.sako14, 'sdss.sako14')
