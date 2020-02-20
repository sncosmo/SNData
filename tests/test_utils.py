#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path
from unittest import TestCase

import numpy as np

from sndata import _utils as utils
from sndata.exceptions import NoDownloadedData


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


class CheckUrl(TestCase):
    """Tests for the ``convert_to_jd`` function"""

    def test_offline_url_warning(self):
        fake_url = 'https://www.thisurllisfake.com/'
        self.assertWarns(Warning, utils.check_url, fake_url)


class RequireDataPath(TestCase):
    """Tests for the ``require_data_path`` function"""

    def test_missing_dir_raises_error(self):
        fake_dir = Path('./This_dir_is_fake')
        self.assertRaises(NoDownloadedData, utils.require_data_path, fake_dir)
