#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``sndata`` package provides access to supernova light-curve data from
various surveys while maintaining a consistent data access interface. Each
available survey is represented by a dedicated submodule. Each available
data release is represented by a dedicated class.
"""

from . import *
from ._combine_data import CombinedDataset, get_zp

__version__ = '1.1.1'
__author__ = 'Daniel Perrefort'
__license__ = 'GPL 3.0'


def delete_all_data():
    """Delete all data downloaded by SNData for all surveys / data releases"""

    from .utils import find_data_dir

    data_dir = find_data_dir('dummy_survey', 'summy_release').parent.parent
    for path in data_dir.glob('*'):
        if path.is_dir():
            path.rmdir()

        else:
            path.unlink()
