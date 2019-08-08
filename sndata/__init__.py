#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This package provides access to supernova light-curve data from various
surveys.
"""

from . import csp, des, essence, sdss
from ._combine_data import CombinedDataset
from ._integrations import parse_snoopy_data
from ._integrations import query_ned_coords
from ._integrations import query_osc
from ._integrations import query_osc_photometry
from ._integrations import query_osc_spectra

__version__ = '0.5.1'
__author__ = 'Daniel Perrefort'
__license__ = 'MIT'


def delete_all_data():
    """Delete all data downloaded by SNData for all surveys / data releases"""

    modules = (csp.dr3, csp.dr1, des.sn3yr, sdss.sako18, essence.narayan16)
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
    modules_dict = {'csp': csp, 'des': des, 'sdss': sdss}
    module = getattr(modules_dict[survey.lower()], release.lower())
    if not hasattr(module, 'band_names'):
        raise ValueError(
            'Survey {} {} does not have registered photometric bandpasses.')

    bands = list(module.band_names)
    zp = module._meta.zero_point
    try:
        i = bands.index(band_name)

    except ValueError:
        raise ValueError(
            f'Could not find band name {band_name} in {module.band_names}')

    return zp[i]
