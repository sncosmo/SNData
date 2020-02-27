#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module provides template testing classes for the user interface of
spectroscopic and photometric data releases.
"""

import re
from pathlib import Path

import yaml

docs_path = Path(__file__).resolve().parent / 'docs.yml'
with open(docs_path) as ofile:
    try:
        expected_docs = yaml.load(ofile, Loader=yaml.FullLoader)

    except AttributeError:  # Support older yaml versions
        expected_docs = yaml.load(ofile)


class VizierTableUI:
    """Generic UI tests for vizier table data releases"""

    pass


class SpectroscopicDataUI(VizierTableUI):
    """Generic UI tests for spectroscopic data releases"""

    def test_not_missing_metadata(self):
        """Test that standard metadata attributes are not null"""

        test_attrs = [
            'survey_name',
            'survey_abbrev',
            'release',
            'survey_url',
            'publications'
        ]

        msg = '``{}`` attribute is not set'
        for attr in test_attrs:
            attr_value = getattr(self.test_class, attr)
            self.assertIsNotNone(attr_value, msg.format(attr))

        self.assertTrue(self.test_class.publications, msg.format('publications'))

    def test_correct_data_type_attribute(self):
        """Test the ``data_type`` attribute is set to ``spectroscopic``"""

        self.assertEqual(self.test_class.data_type, 'spectroscopic')

    def test_consistent_docs(self):
        """Test data access functions have consistent documentation"""

        for func_name, doc_string in expected_docs.items():
            if not hasattr(self.test_class, func_name):
                continue

            # Strip spaces and indentation but not new lines
            class_docs = getattr(self.test_class, func_name)
            func_doc = re.sub("  +", "", class_docs.__doc__)
            expected_doc = re.sub("  +", "", doc_string)

            self.assertEqual(
                expected_doc, func_doc, f'Wrong docstring for ``{func_name}``')


class PhotometricDataUI(SpectroscopicDataUI):
    """Generic UI tests for photometric data releases"""

    def test_not_missing_metadata(self):
        """Test that standard metadata attributes are not null"""

        super().test_not_missing_metadata()

        test_attrs = [
            'band_names',
            'zero_point'
        ]

        msg = '``{}`` attribute is not set'
        for attr in test_attrs:
            attr_value = getattr(self.test_class, attr)
            self.assertTrue(attr_value, msg.format(attr))

    def test_correct_data_type_attribute(self):
        """Test the ``data_type`` attribute is set to ``spectroscopic``"""

        self.assertEqual(self.test_class.data_type, 'photometric')
