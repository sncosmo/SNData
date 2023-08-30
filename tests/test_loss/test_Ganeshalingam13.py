"""Tests for the ``loss.Ganeshalingam13`` class."""

from unittest import TestCase, SkipTest

import requests

from sndata.loss import Ganeshalingam13
from ..common_tests import PhotometricDataParsing, PhotometricDataUI

try:
    Ganeshalingam13().download_module_data()

except requests.exceptions.ConnectionError:
    raise SkipTest('Could not connect to one or more remote servers.')


class Ganeshalingam13Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Ganeshalingam13 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Ganeshalingam13()


class Ganeshalingam13UI(TestCase, PhotometricDataUI):
    """UI tests for the Ganeshalingam13 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Ganeshalingam13()
