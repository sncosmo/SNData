#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to data from the year three DES supernova
cosmology paper. Light curve data is provided from Brout et al. 2018-SMP. The
master_table object provides light curve fit parameters from
Brout et al. 2018-SYS.

No data cuts are applied by this module or its functions.

For more information on DES data products, see:
    https://des.ncsa.illinois.edu/releases/sn
"""

from ._data_access_funcs import get_data_for_id
from ._data_access_funcs import get_input_for_id
from ._data_access_funcs import iter_sncosmo_input
from ._data_access_funcs import master_table
from ._module_meta_data import band_names
from ._module_meta_data import lambda_effective

survey_name = 'DES'
