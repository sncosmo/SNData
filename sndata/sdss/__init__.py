#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``sdss`` module provides access to supernova data from the Sloan
Digital Sky Survey (SDSS). Please note that access to the photometric and
spectroscopic components of the Sako et al. 2018 data release is provided
by separate modules.
"""

from ._sako18 import Sako18
from ._sako18spec import Sako18Spec

survey_name = 'Sloan Digital Sky Survey'
survey_abbrev = 'SDSS'
