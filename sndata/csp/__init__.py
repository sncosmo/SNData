#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``csp`` module provides access to data from the Carnegie Supernova
Project (CSP). It includes data from the first (DR1) and third (DR3) data
releases.
"""

from ._dr1 import DR1
from ._dr3 import DR3

survey_name = 'Carnegie Supernova Project'
survey_abbrev = 'CSP'
