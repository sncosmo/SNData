"""Tests for the ``sdss.Sako18`` class"""

from unittest import TestCase, SkipTest

import requests

from sndata.sdss import Sako18
from ..common_tests import PhotometricDataParsing, PhotometricDataUI

try:
    Sako18().download_module_data()

except requests.exceptions.ConnectionError:
    raise SkipTest('Could not connect to one or more remote servers.')


class Sako18Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Sako18 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Sako18()


class Sako18UI(TestCase, PhotometricDataUI):
    """UI tests for the Sako18 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Sako18()
