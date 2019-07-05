#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Test that survey data is accessed and served correctly for combined data
sets
"""

from SNData import CombinedDataset, csp, des


class Combined():
    """Tests the combined des.sn3yr and csp.dr3 modules"""

    @classmethod
    def setUpClass(cls):
        cls.module = CombinedDataset(csp.dr3, des.sn3yr)
        cls.module.download_module_data()


