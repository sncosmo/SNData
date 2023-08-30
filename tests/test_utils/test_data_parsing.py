"""Tests for the ``data_parsing`` module."""

import os
from pathlib import Path
from unittest import TestCase

import sndata
from sndata.exceptions import NoDownloadedData
from sndata.utils import data_parsing


class FindDataDir(TestCase):
    """Tests for the ``find_data_dir`` function"""

    def test_retrieves_environmental_directory(self):
        """Test the environmental directory is returned if set"""

        expected_path = '/test_dir/survey_abbrev/release'
        _, base_dir, survey, release = expected_path.split('/')

        old_dir = os.environ.get('SNDATA_DIR', None)
        os.environ['SNDATA_DIR'] = f'/{base_dir}'
        recovered_dir = data_parsing.find_data_dir(survey, release)

        if old_dir is None:
            del os.environ['SNDATA_DIR']

        else:
            os.environ['SNDATA_DIR'] = old_dir

        self.assertEqual(Path(expected_path), recovered_dir)

    def test_no_environmental_directory(self):
        """Test a local directory is returned if environment is not set"""

        survey = 'dummy_survey'
        release = 'dummy_release'
        expected_path = Path(sndata.__file__).resolve().parent / 'data' / survey / release
        recovered_dir = data_parsing.find_data_dir(survey, release)
        self.assertEqual(recovered_dir, expected_path)

    def test_enforces_lowercase(self):
        """Test returned directories are always lowercase"""

        survey = 'dummy_survey'
        release = 'dummy_release'
        expected_path = Path(sndata.__file__).resolve().parent / 'data' / survey / release
        recovered_dir = data_parsing.find_data_dir(survey.upper(), release.upper())
        self.assertEqual(recovered_dir, expected_path)


class RequireDataPath(TestCase):
    """Tests for the ``require_data_path`` function"""

    def test_missing_dir_raises_error(self):
        """Test a ``NoDownloadedData`` error is raised"""

        fake_dir = Path('./This_dir_is_fake')
        self.assertRaises(NoDownloadedData, data_parsing.require_data_path, fake_dir)
