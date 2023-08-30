"""Tests for the ``csp.dr1`` class."""

from unittest import TestCase, SkipTest

from requests.exceptions import ConnectionError

from sndata.csp import DR1
from ..common_tests import SpectroscopicDataParsing
from ..common_tests import SpectroscopicDataUI

try:
    DR1().download_module_data()

except ConnectionError:
    raise SkipTest('Could not connect to one or more remote servers.')


class DR1Parsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the DR1 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = DR1()


class DR1UI(TestCase, SpectroscopicDataUI):
    """UI tests for the DR1 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = DR1()
