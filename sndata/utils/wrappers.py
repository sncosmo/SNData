#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``wrappers`` is home to any function or object wrappers used by the
parent package.
"""

import functools
import warnings
from copy import deepcopy
from typing import Union

from tqdm import tqdm


def ignore_warnings_wrapper(func: callable) -> callable:
    """Ignores warnings issued by the wrapped function call"""

    @functools.wraps(func)
    def inner(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            return func(*args, **kwargs)

    return inner


def lru_copy_cache(maxsize: int = 128, typed: bool = False, copy: bool = True):
    """Decorator to cache the return of a function

    Similar to ``functools.lru_cache``, but allows a copy of the cached value
    to be returned, thus preventing mutation of the cache.

    Args:
        maxsize: Maximum size of the cache
        typed: Cache objects of different types separately (Default: False)
        copy: Return a copy of the cached item (Default: True)

    Returns:
        A decorator
    """

    if not copy:
        # Return the normal function cache
        return functools.lru_cache(maxsize, typed)

    # noinspection PyMissingOrEmptyDocstring
    def decorator(f):
        cached_func = functools.lru_cache(maxsize, typed)(f)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return deepcopy(cached_func(*args, **kwargs))

        return wrapper

    return decorator


def build_pbar(data: iter, verbose: Union[bool, dict]):
    """Cast an iterable into a progress bar

    If verbose is False, return ``data`` unchanged.

    Args:
        data: An iterable object
        verbose: Arguments for tqdm.tqdm
    """

    if isinstance(verbose, dict):
        iter_data = tqdm(data, **verbose)

    elif verbose:
        iter_data = tqdm(data)

    else:
        iter_data = data

    return iter_data
