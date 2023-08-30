"""Tests for the ``snls.Balland09`` class"""

from unittest import TestCase, SkipTest
from unittest import skip

import requests

from sndata.snls import Balland09
from ..common_tests import SpectroscopicDataParsing
from ..common_tests import SpectroscopicDataUI

try:
    Balland09().download_module_data()

except requests.exceptions.ConnectionError:
    raise SkipTest('Could not connect to one or more remote servers.')


class Balland09Parsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the Balland09 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Balland09()

    @skip('Balland09 data tables do not have dates')
    def test_jd_time_format(self):
        pass

    def test_standard_column_names(self):
        """Test columns required by sncosmo are included in formatted tables

        Columns checked to exist include:
            'phase', 'band', 'flux'
        """

        test_id = self.test_class.get_available_ids()[0]
        test_data = self.test_class.get_data_for_id(test_id, format_table=True)

        expected_cols = ('phase', 'wavelength', 'flux')
        for column in expected_cols:
            self.assertIn(column, test_data.colnames)


class Balland09UI(TestCase, SpectroscopicDataUI):
    """UI tests for the Balland09 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Balland09()
