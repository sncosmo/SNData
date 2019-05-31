#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test input data used for fitting light-curves with SNCosmo."""

from unittest import TestCase

from SNData import csp

csp.dr1.download_module_data()
csp.dr3.download_module_data()


# noinspection PyPep8Naming
class T0_EmptyTables(TestCase):
    """Test for any empty tables iterating of data tables"""

    def _test_module(self, module, name):
        """Generic function to test a given module

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

    def test_csp_dr1(self):
        self._test_module(csp.dr1, 'csp.dr1')

    def test_csp_dr3(self):
        self._test_module(csp.dr3, 'csp.dr3')


# noinspection PyPep8Naming
class T1_DeleteData(TestCase):
    """Test that data is deleted when ``delete_module_data`` is called"""

    def _test_module(self, module, name):
        """Generic function to test a given module

        Args:
            module (module): A data access module
            name      (str): Name of ``module`` for error message
        """

        if not module.data_is_available():
            raise RuntimeError(
                f'No data found for {name}. Cannot test deletion.')

        module.delete_module_data()
        self.assertFalse(module.data_is_available(), f'Test failed for {name}')

    def test_csp_dr1(self):
        self._test_module(csp.dr1, 'csp.dr1')

    def test_csp_dr3(self):
        self._test_module(csp.dr3, 'csp.dr3')
