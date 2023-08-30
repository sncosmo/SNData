"""Tests for the ``unit_conversion`` module."""

from unittest import TestCase

import numpy as np

from sndata.utils import unit_conversion as uc


class HourangleToDegrees(TestCase):
    """Tests for the ``hourangle_to_degrees`` function"""

    def test_coordinates_0_0(self):
        """Test a zero hourangle returns zero degrees"""

        ra, dec = uc.hourangle_to_degrees(0, 0, 0, '+', 0, 0, 0)
        self.assertEqual(0, ra)
        self.assertEqual(0, dec)


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
            self.expected_jd, uc.convert_to_jd(self.snoopy_date, 'snpy'),
            'Incorrect date for snoopy format')

    def test_mjd_format(self):
        """Test conversion of the MJD format to JD"""

        self.assertEqual(
            self.expected_jd, uc.convert_to_jd(self.mjd_date, 'mjd'),
            'Incorrect date for MJD format')
