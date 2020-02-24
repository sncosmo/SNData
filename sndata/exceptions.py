#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines custom exceptions."""


class NoDownloadedData(Exception):
    def __init__(self, *args, **kwargs):
        default_message = 'Data has not been downloaded for this data release.'
        args = args if args else (default_message,)
        super().__init__(*args, **kwargs)


class InvalidObjId(Exception):
    def __init__(self, *args, **kwargs):
        args = args if args else ('The provided object Id is not valid.',)
        super().__init__(*args, **kwargs)


class ObservedDataTypeError(Exception):
    def __init__(self, *args, **kwargs):
        # Add default message
        default_message = (
            'This action is not valid for the type of data '
            'included in the current data release.',
        )
        args = args if args else (default_message,)
        super().__init__(*args, **kwargs)
