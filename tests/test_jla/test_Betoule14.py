"""Tests for the ``jla.Betoule14`` class"""

from unittest import TestCase, SkipTest

import requests

from sndata.jla import Betoule14
from ..common_tests import PhotometricDataParsing, PhotometricDataUI

try:
    Betoule14().download_module_data()

except requests.exceptions.ConnectionError:
    raise SkipTest('Could not connect to one or more remote servers.')


class Betoule14Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Betoule14 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Betoule14()


class Betoule14UI(TestCase, PhotometricDataUI):
    """UI tests for the Betoule14 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Betoule14()
