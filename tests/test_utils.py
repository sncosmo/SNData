#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

import numpy as np

from sndata import _utils as utils


class ConvertToJD(TestCase):
    """Tests for the ``convert_to_jd`` function"""

    @classmethod
    def setUpClass(cls):
        """Define test dates"""

        cls.snoopy_date = 500
        cls.mjd_date = cls.snoopy_date + 53000
        cls.jd_date = cls.mjd_date + 2400000.5
        cls.expected_jd = np.array(cls.jd_date)

    def test_snoopy_format(self):
        """Test conversion of the snoopy date format to JD"""

        self.assertEqual(
            self.expected_jd, utils.convert_to_jd(self.snoopy_date),
            'Incorrect date for snoopy format')

    def test_mjd_format(self):
        """Test conversion of the MJD format to JD"""

        self.assertEqual(
            self.expected_jd, utils.convert_to_jd(self.mjd_date),
            'Incorrect date for MJD format')

    def test_jd_format(self):
        """Test conversion of the JD format to JD"""

        self.assertEqual(
            self.expected_jd, utils.convert_to_jd(self.jd_date),
            'Incorrect date for JD format')


class CreateDataDir(TestCase):
    """Tests for the ``convert_to_jd`` function"""

    @classmethod
    def setUpClass(cls):
        """Create a temporary directory and add it to the environment"""
        cls.test_dir = TemporaryDirectory()
        cls.old_environ = environ.copy()
        environ['SNDATA_DIR'] = cls.test_dir.name

    @classmethod
    def tearDownClass(cls):
        cls.test_dir.cleanup()
        del environ['SNDATA_DIR']
        environ.update(cls.old_environ)

    # Todo: Fail on Mac OS
    def test_directories_are_created(self):
        """Test the function creates subdirectories with the expected naming structure"""

        survey_name = 'dummy_survey'
        release_name = 'dummy_release'
        expected_path = Path(self.test_dir.name) / survey_name / release_name
        created_path = utils.create_data_dir(survey_name, release_name)

        self.assertEqual(expected_path, created_path, 'Directory does not match expected name')
        self.assertTrue(created_path.exists(), 'Directory does not exist')

    def test_spaces_stripped_from_names(self):
        """Test spaces are stripped before creatign the directories"""

        survey_name = 'survey with spaces'
        release_name = 'release with spaces'
        created_path = utils.create_data_dir(survey_name, release_name)
        self.assertFalse(' ' in str(created_path), 'Directory name has spaces')
