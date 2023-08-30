"""Tests for the ``sdss.Sako18Spec`` class"""

from unittest import TestCase

from sndata.sdss import Sako18Spec
from ..common_tests import SpectroscopicDataParsing, SpectroscopicDataUI, download_data_or_skip

download_data_or_skip(Sako18Spec())


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
