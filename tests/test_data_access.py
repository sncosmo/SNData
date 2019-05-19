#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test input data used for fitting light-curves with SNCosmo."""

from itertools import islice
from unittest import TestCase

import numpy as np

from SNData import csp, des, sdss


class EmptyInputTables(TestCase):
    """Test for any empty tables when fitting DES and SDSS data"""

    def _check_module(self, module):
        """Generic function to check for empty SNCosmo input tables

        Only checks the first 20 tables.

        Args:
            module (module): A data access module
        """

        err_msg = 'Empty table for {} cid {}.'
        for input_table in islice(module.iter_sncosmo_input(), 20):
            cid = input_table.meta['cid']
            self.assertTrue(
                input_table,
                msg=err_msg.format(module.survey_name, cid))

    def runTest(self):
        """Test the first 20 inputs aren't empty for CSP, DES, and SDSS"""

        for module in (csp, des, sdss):
            self._check_module(module)


class ZeroPoint(TestCase):
    """Test for correct zero points when fitting DES and SDSS data"""

    def _check_module(self, module, expected_zero):
        """Generic function to check zero point of an SNCosmo input tables

        Only checks the first 20 tables.

        Args:
            module       (module): A data access module
            expected_zero (float): The expected zero point
        """

        err_msg = 'Incorrect zero point for {} cid {}. Found {}, expected {}'
        for table in islice(module.iter_sncosmo_input(), 20):
            cid = table.meta['cid']
            correct_zero = table['zp'] == expected_zero

            if not all(correct_zero):
                bad_indices = np.logical_not(correct_zero)
                example_val = table['zp'][bad_indices][0]
                self.fail(err_msg.format(cid, example_val, expected_zero))

    def runTest(self):
        """Check the zero points of the first 20 inputs for DES and SDSS

        Expects DES zero point of 27.5
        Expects SDSS zero point of 3.56
        """

        modules = (des, sdss)
        zero_points = (27.5, 2.5 * np.log10(3631))

        for m, zp in zip(modules, zero_points):
            self._check_module(m, zp)
