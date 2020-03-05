#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines custom exceptions."""


class NoDownloadedData(Exception):
    """Error for when data is requested that has not been downloaded"""

    def __init__(self, *args, **kwargs):
        default_message = 'Data has not been downloaded for this data release.'
        args = args if args else (default_message,)
        super().__init__(*args, **kwargs)


class InvalidObjId(Exception):
    """Error for when data is requested for an unknown object Id"""

    def __init__(self, *args, **kwargs):
        args = args if args else ('The provided object Id is not valid.',)
        super().__init__(*args, **kwargs)


class InvalidTableId(Exception):
    """Error for when data is requested for an unknown table Id"""

    def __init__(self, *args, **kwargs):
        args = args if args else ('No table was found matching the given ID.',)
        super().__init__(*args, **kwargs)


class ObservedDataTypeError(Exception):
    """Error for when an action is requested that is not available for a
     type of astronomical data."""

    def __init__(self, *args, **kwargs):
        # Add default message
        default_message = (
            'This action is not valid for the type of data '
            'included in the current data release.',
        )
        args = args if args else (default_message,)
        super().__init__(*args, **kwargs)
