#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test that survey data is accessed and served correctly"""

from pathlib import Path
from unittest import TestCase
from warnings import warn

import requests
import yaml

from sndata import csp, des, essence, sdss

docs_path = Path(__file__).resolve().parent / 'docs.yml'
with open(docs_path) as ofile:
    try:
        expected_docs = yaml.load(ofile, Loader=yaml.FullLoader)

    except AttributeError:  # Support older yaml versions
        expected_docs = yaml.load(ofile)


class GeneralTests(TestCase):
    """Generic tests for a given survey"""

    def _test_consistent_docs(self, skip_funcs=()):
        """Test data access functions have consistent documentation

        Args:
            skip_funcs (iter[str]): Function names to skip during testing
        """

        for func_name, doc_string in expected_docs.items():
            if func_name not in skip_funcs:
                module_func = getattr(self.module, func_name)
                self.assertEqual(doc_string, module_func.__doc__,
                                 f'Wrong docstring for ``{func_name}``')

    def _test_ads_url(self):
        """Test module.ads_url returns a 200 status code"""

        stat_code = requests.get(self.module.ads_url).status_code
        if not stat_code == 200:
            warn(f'Error code {stat_code}: {self.module.survey_url}')

    def _test_survey_url(self):
        """Test module.survey_url returns a 200 status code"""

        stat_code = requests.get(self.module.survey_url).status_code
        if not stat_code == 200:
            warn(f'Error code {stat_code}: {self.module.survey_url}')


class CSP_DR1(GeneralTests):
    """Tests for the csp.dr1 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr1

    def test_consistent_docs(self):
        self._test_consistent_docs(
            skip_funcs=('register_filters'))

    def test_ads_url(self):
        self._test_ads_url()

    def test_survey_url(self):
        self._test_survey_url()


class CSP_DR3(GeneralTests):
    """Tests for the csp.dr3 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr3

    def test_consistent_docs(self):
        self._test_consistent_docs()

    def test_ads_url(self):
        self._test_ads_url()

    def test_survey_url(self):
        self._test_survey_url()


class SDSS_Sako18(GeneralTests):
    """Tests for the sdss.sako18 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = sdss.sako18

    def test_consistent_docs(self):
        self._test_consistent_docs()

    def test_ads_url(self):
        self._test_ads_url()

    def test_survey_url(self):
        self._test_survey_url()


class DES_SN3YR(GeneralTests):
    """Tests for the des.SN3YR module"""

    @classmethod
    def setUpClass(cls):
        cls.module = des.sn3yr

    def test_consistent_docs(self):
        self._test_consistent_docs()

    def test_ads_url(self):
        self._test_ads_url()

    def test_survey_url(self):
        self._test_survey_url()


class ESSENCE_Narayan16(GeneralTests):
    """Tests for the essence.narayan16 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = essence.narayan16

    def test_consistent_docs(self):
        self._test_consistent_docs()

    def test_ads_url(self):
        self._test_ads_url()

    def test_survey_url(self):
        self._test_survey_url()
