#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test that SNData interfaces with SNCosmo correctly.
Tests are run using csp.dr3
"""

from unittest import TestCase
from warnings import warn

import sncosmo
from requests.exceptions import HTTPError

from sndata import csp, query_ned_coords, query_osc, query_osc_photometry, \
    query_osc_spectra


class SNCosmo(TestCase):
    """Tests for integrated SNCosmo services"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr3
        cls.module.download_module_data()

    def test_filter_registration(self):
        """Test csp registered bands do not have empty names"""

        self.module.register_filters()
        for band_name in self.module.band_names:
            sncosmo_band = sncosmo.get_bandpass(band_name)
            self.assertEqual(band_name, sncosmo_band.name)


class NED(TestCase):
    """Tests for integrated NED services"""

    def test_prefix_independence(self):
        """Test results are returned regardless of 'SN' prefix"""

        try:
            no_prefix = query_ned_coords('2011fe')
            lower_prefix = query_ned_coords('sn2011fe')
            upper_prefix = query_ned_coords('SN2011fe')

            self.assertEqual(no_prefix, lower_prefix)
            self.assertEqual(lower_prefix, upper_prefix)

        except HTTPError:
            warn('Could not reach NED.')


class OSC(TestCase):
    """Tests for integrated NED services"""

    @classmethod
    def setUpClass(cls):
        cls.test_id = '2011fe'

    def test_general_query(self):
        """Test queries for an object's metadata"""

        self.assertTrue(query_osc(self.test_id))

    def test_photometry_query(self):
        """Test queries for an object's photometric data"""

        self.assertTrue(query_osc_photometry(self.test_id))

    def test_spectra_query(self):
        """Test queries for an object's spectroscopic data"""

        self.assertTrue(query_osc_spectra(self.test_id))
