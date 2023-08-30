"""Tests for the ``csp.DR3`` class."""

from unittest import TestCase

import numpy as np

from sndata.csp import DR3
from ..common_tests import PhotometricDataParsing, PhotometricDataUI, download_data_or_skip

download_data_or_skip(DR3())


class DR3Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the DR3 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = DR3()

    def test_instrument_offsets_ar_applied(self):
        """Test returned DR3 data includes the instrument offset using a
         single data point from 2005el.
         """

        def get_test_point(band, obj_id='2005el', **kwargs):
            data = DR3().get_data_for_id(obj_id, **kwargs)
            y_data = data[data['band'] == band]
            return y_data[0]

        unformatted_data = get_test_point('Y', '2005el', format_table=False)
        formatted_data = get_test_point('csp_dr3_Y', '2005el')

        # Check magnitude offset from natural to AB mag
        offset = np.round(formatted_data['mag'] - unformatted_data['mag'], 4)
        Yband_offset = 0.63  # From Krisciunas et al. 2017
        self.assertEqual(offset, Yband_offset)

        # Check error in mag is not changed
        self.assertEqual(formatted_data['mag_err'], unformatted_data['mag_err'])


class DR3UI(TestCase, PhotometricDataUI):
    """UI tests for the DR3 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = DR3()
