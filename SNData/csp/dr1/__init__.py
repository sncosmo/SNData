#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module provides access to spectra from the first data release of the
Carnegie Supernova Project (CSP).
"""

from ._data_download import data_is_available
from ._data_download import delete_module_data
from ._data_download import download_module_data
from ._data_parsing import get_available_ids
from ._data_parsing import get_available_tables
from ._data_parsing import get_data_for_id
from ._data_parsing import iter_data
from ._data_parsing import load_table

data_type = 'spectroscopy'
publication = 'Folatelli et al. (2013)'
arxiv = 'https://arxiv.org/abs/1305.6997'
