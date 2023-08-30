"""This module defines reusable setup and testing logic for streamlining the
creation of downstream tests.
"""
from unittest import SkipTest

from .data_parsing_tests import *
from .ui_tests import *


def download_data_or_skip(release) -> None:
    """Download data for the given data release. Skip any further tests if the download fails"""

    try:
        release.download_module_data()

    except ConnectionError:
        raise SkipTest('Could not connect to one or more remote servers.')
