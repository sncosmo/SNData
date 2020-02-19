#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This package provides access to supernova light-curve data from various
surveys.
"""

# from . import csp, des, essence, jla, sdss
# from ._combine_data import CombinedDataset
from .exceptions import ObservedDataTypeError as _ObservedDataTypeError
from . import csp, des, essence, jla

__version__ = '0.9.5'
__author__ = 'Daniel Perrefort'
__license__ = 'GPL 3.0'


def delete_all_data():
    """Delete all data downloaded by SNData for all surveys / data releases"""

    modules = (
        csp.DR1(),
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
    modules_dict = {
        'dr1': csp.DR1,
        'dr3': csp.DR3,
        'sn3yr': des.SN3YR,
        'narayan16': essence.Narayan16,
        'betoule14': jla.Betoule14,
    }

    data_class = modules_dict[release]
    if not hasattr(data_class, 'band_names'):
        raise _ObservedDataTypeError(
            'Survey {} {} does not have registered photometric band passes.')

    return data_class.get_zp_for_band(band_name)
