#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This package provides access to supernova light-curve data from various
surveys.
"""

from . import csp, des, essence, sdss
from ._combine_data import CombinedDataset
from .exceptions import ObservedDataTypeError as _ObservedDataTypeError

__version__ = '0.8.2'
__author__ = 'Daniel Perrefort'
__license__ = 'GPL 3.0'


def delete_all_data():
    """Delete all data downloaded by SNData for all surveys / data releases"""

    modules = (
        csp.dr3, csp.dr1, des.sn3yr, essence.narayan16,
        sdss.sako18, sdss.sako18spec,
    )

    for module in modules:
        module.delete_module_data()


def get_zp(band_name):
    """Return the zero point used by sndata for a given bandpass

    bandpass names are case sensitive.

    Args:
        band_name (str): The name of the sndata bandpass

    Returns:
        The zero point as a float
    """

    survey, release, *_ = band_name.split('_')
    modules_dict = {'csp': csp, 'des': des, 'sdss': sdss, 'essence': essence}
    module = getattr(modules_dict[survey.lower()], release.lower())
    if not hasattr(module, 'band_names'):
        raise _ObservedDataTypeError(
            'Survey {} {} does not have registered photometric band passes.')

    bands = list(module.band_names)
    zp = module._meta.zero_point

    try:
        i = bands.index(band_name)

    except ValueError:
        raise ValueError(
            f'Could not find band name {band_name} in {module.band_names}')

    return zp[i]
