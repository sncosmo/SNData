#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from unittest import TestCase

from sndata.exceptions import InvalidObjId, InvalidTableId, NoDownloadedData, ObservedDataTypeError


class NonEmptyDefaultMessage(TestCase):
    """Test custom exceptions have default messages"""

    @classmethod
    def setUpClass(cls):
        cls.exceptions = NoDownloadedData, InvalidObjId, ObservedDataTypeError, InvalidTableId

    def runTest(self):
        for exception in self.exceptions:
            try:
                raise exception

            except Exception as e:
                self.assertTrue(str(e), f'Exception {exception.__name__} has no default message')
