"""Tests for the ``essence.Narayan16`` class."""

from unittest import TestCase, SkipTest

import requests

from sndata.essence import Narayan16
from ..common_tests import PhotometricDataParsing, PhotometricDataUI

try:
    Narayan16().download_module_data()

except requests.exceptions.ConnectionError:
    raise SkipTest('Could not connect to one or more remote servers.')


class Narayan16Parsing(TestCase, PhotometricDataParsing):
    """Data parsing tests for the Narayan16 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Narayan16()


class Narayan16UI(TestCase, PhotometricDataUI):
    """UI parsing tests for the Narayan16 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Narayan16()
