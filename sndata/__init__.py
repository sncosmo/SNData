#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``sndata`` package provides access to supernova light-curve data from
various surveys while maintaining a consistent data access interface. Each
available survey is represented by a dedicated submodule. Each available
data release is represented by a dedicated class.
"""

from . import csp, des, essence, jla, sdss
from ._combine_data import CombinedDataset, get_zp
from .exceptions import ObservedDataTypeError as _ObservedDataTypeError

__version__ = '0.10.0'
__author__ = 'Daniel Perrefort'
__license__ = 'GPL 3.0'


def delete_all_data():
    """Delete all data downloaded by SNData for all surveys / data releases"""

    data_classes = (
        csp.DR1(),
        csp.DR1(),
        des.SN3YR(),
        essence.Narayan16(),
        jla.Betoule14(),
        sdss.Sako18(),
        sdss.Sako18Spec()
    )

    for data_class in data_classes:
        data_class.delete_module_data()



