#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``bsnip`` module provides access to data from the Berkeley Supernova
Ia Program (BSNIP). For the photometric compliment to this survey, see the
``loss`` module.
"""

from ._stahl20 import Stahl20
from ._Silverman12 import Silverman12

survey_name = 'Berkeley Supernova Ia Program'
survey_abbrev = 'BSNIP'
