#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from pathlib import Path
from unittest import TestCase

import numpy as np

from sndata import utils as utils
from sndata.exceptions import NoDownloadedData


class HourangleToDegrees(TestCase):
    """Tests for the ``hourangle_to_degrees`` function"""

    def test_coordinates_0_0(self):
        """Test a zero hourangle returns zero degrees"""

        ra, dec = utils.hourangle_to_degrees(0, 0, 0, '+', 0, 0, 0)
        self.assertEqual(0, ra)
        self.assertEqual(0, dec)


class FindDataDir(TestCase):
    """Tests for the ``find_data_dir`` function"""

    def test_retrieves_environmental_directory(self):
        """Test the environmental directory is returned if set"""

        expected_path = '/test_dir/survey_abbrev/release'
        _, base_dir, survey, release = expected_path.split('/')

        old_dir = os.environ.get('SNDATA_DIR', None)
        os.environ['SNDATA_DIR'] = f'/{base_dir}'
        recovered_dir = utils.find_data_dir(survey, release)

        if old_dir is None:
            del os.environ['SNDATA_DIR']

        else:
            os.environ['SNDATA_DIR'] = old_dir

        self.assertEqual(Path(expected_path), recovered_dir)

    def test_no_environmental_directory(self):
        """Test a local directory is returned if environment is not set"""

        survey = 'dummy_survey'
        release = 'dummy_release'
        expected_path = Path(utils.__file__).resolve().parent / 'data' / survey / release
        recovered_dir = utils.find_data_dir(survey, release)
        self.assertEqual(expected_path, recovered_dir)

    def test_enforces_lowercase(self):
        """Test returned directories are always lowercase"""

        survey = 'dummy_survey'
        release = 'dummy_release'
        expected_path = Path(utils.__file__).resolve().parent / 'data' / survey / release

        recovered_dir = utils.find_data_dir(survey.upper(), release.upper())
        self.assertEqual(expected_path, recovered_dir)


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


class RequireDataPath(TestCase):
    """Tests for the ``require_data_path`` function"""

    def test_missing_dir_raises_error(self):
        """Test a ``NoDownloadedData`` error is raised"""

        fake_dir = Path('./This_dir_is_fake')
        self.assertRaises(NoDownloadedData, utils.require_data_path, fake_dir)
