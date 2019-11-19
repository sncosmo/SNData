#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines custom exceptions."""


class NoDownloadedData(Exception):
    def __init__(self, *args, **kwargs):
        default_message = \
            'Data has not been downloaded for this module / data release.'

        if not (args or kwargs):
            args = (default_message,)

        super().__init__(*args, **kwargs)


class InvalidObjId(Exception):
    def __init__(self, *args, **kwargs):
        default_message = 'The provided object Id is not valid.'

        if not (args or kwargs):
            args = (default_message,)

        super().__init__(*args, **kwargs)


class ObservedDataTypeError(Exception):
    def __init__(self, *args, **kwargs):
        default_message = (
            'This action is not valid for the type of data '
            'included in the current data release.'
        )

        if not (args or kwargs):
            args = (default_message,)

        super().__init__(*args, **kwargs)
