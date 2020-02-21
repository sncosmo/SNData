#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``jla`` module provides access to supernova data compiled by the
Joint Light-Curve Analysis project. It includes recalibrated light-curves
of type Ia supernova (SN Ia) from the SDSS-II and SNLS collaborations.
"""

from ._betoule14 import Betoule14

survey_name = 'Joint Light-Curve Analysis'
survey_abbrev = 'JLA'
