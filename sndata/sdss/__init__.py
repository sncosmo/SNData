#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""The ``sdss`` module provides access to supernova data from the Sloan
Digital Sky Survey (SDSS). Please note that access to the photometric and
spectroscopic components of the Sako et al. 2018 data release is provided
by separate modules. For more information on SDSS see https://www.sdss.org .
"""

from . import sako18, sako18spec

survey_name = 'Sloan Digital Sky Survey'
survey_abbrev = 'SDSS'
