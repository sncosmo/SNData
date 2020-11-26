#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``unit_conversion`` handles the conversion of values between different
units / timezones / systems of measurement.
"""

from datetime import datetime

import numpy as np
from astropy.coordinates import Angle
from pytz import utc


def hourangle_to_degrees(
        rah: float,
        ram: float,
        ras: float,
        dec_sign: str,
        decd: float,
        decm: float,
        decs: float) -> (float, float):
    """Convert from hour angle to degrees

    Args:
        rah: RA hours
        ram: RA arcminutes
        ras: RA arcseconds
        dec_sign: Sign of the declination ('+' or '-')
        decd: Dec degrees
        decm: Dec arcmin
        decs: Dec arcsec
    """

    # Convert Right Ascension
    ra = Angle((rah, ram, ras), unit='hourangle').to('deg').value

    # Convert Declination
    sign = -1 if dec_sign == '-' else 1
    dec = (
            sign * decd +  # Already in degrees
            decm / 60 +  # arcmin to degrees
            decs / 60 / 60  # arcesc to degrees
    )
    return ra, dec


@np.vectorize
def convert_to_jd(date: float, format: str) -> float:
    """Convert dates into JD

    Can convert the Snoopy, MJD, or UT time standards.

    Args:
        date: Time stamp value
        format: Either ``snpy``, ``mjd``, or ``ut``

    Returns:
        The time value in JD format
    """

    snoopy_offset = 53000  # Conversion from Snoopy to MJD
    mjd_offset = 2400000.5  # Conversion from MJD to JD

    if format.lower() == 'snpy':
        return date + snoopy_offset + mjd_offset

    elif format.lower() == 'mjd':
        return date + mjd_offset

    elif format.lower() == 'ut':
        # Break date down into year, month, and days
        str_date = str(date)
        year = int(str_date[:4])
        month = int(str_date[4:6])
        day = int(str_date[6:8])
        fractional_days = float(str_date[8:])

        # Convert fractional days into minutes and seconds
        hours_in_day = 24
        min_in_hour = 60
        sec_in_min = 60
        microsec_in_sec = 1e+6

        hours = fractional_days * hours_in_day
        minutes = (hours * min_in_hour) - (int(hours) * min_in_hour)
        seconds = (minutes * sec_in_min) - (int(minutes) * sec_in_min)
        microsec = (seconds * microsec_in_sec) - (int(seconds) * microsec_in_sec)

        # ``toordinal`` returns the number of days since December 31, 1 BC
        # We add 1721424.5 to rescale the result to January 1, 4713 BC at 12:00 (i.e. to JD)
        date = datetime(year, month, day, int(hours), int(minutes), int(seconds), int(microsec), tzinfo=utc)
        return date.toordinal() + 1721424.5

    raise NotImplementedError(f'Cannot convert format: {format}')
