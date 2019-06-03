#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test that SNData interfaces with SNCosmo correctly"""

from unittest import TestCase

import sncosmo

from SNData import csp


class FilterRegistration(TestCase):
    """Test survey filters are registered"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr3
        cls.module.download_module_data()

    def test_band_names(self):
        """Test bands do not have empty names"""

        self.module.register_filters()
        for band_name in self.module.band_names:
            sncosmo_band = sncosmo.get_bandpass(band_name)
            self.assertEqual(band_name, sncosmo_band.name)
