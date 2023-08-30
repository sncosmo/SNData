"""Tests for the ``sdss.Sako18Spec`` class"""

from unittest import TestCase, SkipTest

import requests

from sndata.sdss import Sako18Spec
from ..common_tests import SpectroscopicDataParsing
from ..common_tests import SpectroscopicDataUI

try:
    Sako18Spec().download_module_data()

except requests.exceptions.ConnectionError:
    raise SkipTest('Could not connect to one or more remote servers.')


class Sako18SpecParsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the Sako18Spec release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Sako18Spec()


class Sako18SpecUI(TestCase, SpectroscopicDataUI):
    """UI tests for the Sako18Spec release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Sako18Spec()
