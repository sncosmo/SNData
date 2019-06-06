#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Utilities for querying the Open Supernova Catalog."""

import json

import requests
from astropy.table import Table


def _query_osc(uia_name, data_type, query_vals):
    if not uia_name.lower().startswith('sn'):
        uia_name = "SN" + uia_name
    url = (f'https://api.astrocats.space/{uia_name}/{data_type}/'
           f'{"+".join(query_vals)}')
    response = requests.get(url)
    response.raise_for_status()
    data = json.loads(response.content.decode('utf-8'))[uia_name][data_type]
    return data


def query_osc_photometry(uia_name, values=()):
    """Return photometric data from the Open Supernova Catalog

    Returns all available data by default. Specific data fields can be
    requested using the ``values`` argument. For a summary of available
    fields, see: https://github.com/astrocatalogs/schema

    Args:
        uia_name     (str): SN name (e.g. ['SN2011fe'])
        values (list[str]): List of additional fields to query

    Returns:
        An astropy table of photometric data from the OSC
    """

    values = set(values)
    return Table(rows=_query_osc(uia_name, 'photometry', values), names=values)


def query_osc_spectra(uia_name, values=()):
    """Return photometric data from the Open Supernova Catalog

    Specific data fields can be requested using the ``values`` argument.
    Default values include: 'band', 'zeropoint', 'observatory', 'telescope',
    'survey', 'instrument', 'system', 'magnitude', 'e_magnitude', 'time'

    For a summary of available fields, see:
    https://github.com/astrocatalogs/schema

    Args:
        uia_name     (str): SN name (e.g. ['SN2011fe'])
        values (list[str]): List of additional fields to query

    Returns:
        A list of spectral data as dictionaries
    """

    values = set(values)
    return _query_osc(uia_name, 'spectra', values)
