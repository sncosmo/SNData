#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides template testing classes for the user interface of
spectroscopic and photometric data releases.
"""


class SpectroscopicDataUI:
    """Generic UI tests for spectroscopic data releases"""

    def test_not_missing_metadata(self):
        """Test that standard metadata attributes are not null"""

        test_attrs = [
            'survey_name',
            'survey_abbrev',
            'release',
            'survey_url',
            'ads_url',
            'publications',
        ]

        msg = '``{}`` attribute is not set'
        for attr in test_attrs:
            attr_value = getattr(self.test_class, attr)
            self.assertTrue(attr_value, msg.format(attr))

    def test_correct_data_type_attribute(self):
        """Test the ``data_type`` attribute is set to ``spectroscopic``"""

        self.assertEqual(self.test_class.data_type, 'spectroscopic')


class PhotometricDataUI(SpectroscopicDataUI):
    """Generic UI tests for photometric data releases"""

    def test_not_missing_metadata(self):
        """Test that standard metadata attributes are not null"""

        test_attrs = [
            'survey_name',
            'survey_abbrev',
            'release',
            'survey_url',
            'ads_url',
            'publications',
            'band_names',
            'zero_point'
        ]

        msg = '``{}`` attribute is not set'
        for attr in test_attrs:
            attr_value = getattr(self.test_class, attr)
            self.assertTrue(attr_value, msg.format(attr))

    def test_correct_data_type_attribute(self):
        """Test the ``data_type`` attribute is set to ``photometric``"""

        self.assertEqual(self.test_class.data_type, 'photometric')
