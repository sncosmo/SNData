"""This module parses spectroscopic data from a fits file written in
the IRAF multispec format. Parsing includes the ability to read most multispec
formats including linear, log, cubic spline, Chebyshev or Legendre dispersion
spectra

This code is was originally written by Rick White and then shared with
Kevin Gullikson who distributed it publicly under a GPL-3.0 licence.
Minor modifications to the public code were made after adopting the code here
in order to improve readability and port the code from Python 2 to Python 3.
Original Code: https://github.com/kgullikson88/General
"""

import numpy as np
from astropy.io import fits as pyfits


def nonlinear_wave(nwave, specstr, verbose=False):
    """Compute non-linear wavelengths from multispec string

    Args:
        nwave    (int): Number of wavelength values to return
        specstr:
        verbose (bool): Print status while parsing

    Returns:
        An array of wavelength values
        The dispersion fields
    """

    fields = specstr.split()
    if int(fields[2]) != 2:
        raise ValueError(f'Not nonlinear dispersion: dtype={fields[2]}')

    if len(fields) < 12:
        raise ValueError(f'Bad spectrum format (only {len(fields)} fields)')

    ftype = int(fields[11])
    if ftype == 3:  # Cubic spline
        if len(fields) < 15:
            raise ValueError(f'Bad spline format (only {len(fields)} fields)')

        npieces = int(fields[12])
        pmin = float(fields[13])
        pmax = float(fields[14])
        if verbose:
            print(f'Dispersion is order-{npieces} cubic spline')

        if len(fields) != 15 + npieces + 3:
            raise ValueError(
                f'Bad order-{npieces} spline format ({len(fields)} fields)')

        coefficients = np.asarray(fields[15:], dtype=float)

        # Normalized x coordinates
        s = (np.arange(nwave, dtype=float) + 1 - pmin) / (pmax - pmin) * npieces
        j = s.astype(int).clip(0, npieces - 1)
        a = (j + 1) - s
        b = s - j
        x0 = a ** 3
        x1 = 1 + 3 * a * (1 + a * b)
        x2 = 1 + 3 * b * (1 + a * b)
        x3 = b ** 3
        wave = (
                coefficients[j] * x0 +
                coefficients[j + 1] * x1 +
                coefficients[j + 2] * x2 +
                coefficients[j + 3] * x3
        )

    elif ftype == 1 or ftype == 2:
        # chebyshev or legendre polynomial
        # legendre not tested yet
        if len(fields) < 15:
            raise ValueError(
                f'Bad polynomial format (only {len(fields)} fields)')

        order = int(fields[12])
        pmin = float(fields[13])
        pmax = float(fields[14])
        if verbose:
            if ftype == 1:
                print(f'Dispersion is order-{order} Chebyshev polynomial')

            else:
                print(f'Dispersion is order-{order} Legendre polynomial (NEEDS TEST)')

        if len(fields) != 15 + order:
            # raise ValueError('Bad order-%d polynomial format (%d fields)' % (order, len(fields)))
            if verbose:
                print(f'Bad order-{order} polynomial format ({len(fields)} fields)')
                print(f'Changing order from {order} to {len(fields) - 15}')

            order = len(fields) - 15

        coefficients = np.asarray(fields[15:], dtype=float)

        # normalized x coordinates
        pmiddle = (pmax + pmin) / 2
        prange = pmax - pmin
        x = (np.arange(nwave, dtype=float) + 1 - pmiddle) / (prange / 2)
        p0 = np.ones(nwave, dtype=float)
        p1 = x
        wave = p0 * coefficients[0] + p1 * coefficients[1]

        for i in range(2, order):
            if ftype == 1:  # chebyshev
                p2 = 2 * x * p1 - p0

            else:  # legendre
                p2 = ((2 * i - 1) * x * p1 - (i - 1) * p0) / i

            wave = wave + p2 * coefficients[i]
            p0 = p1
            p1 = p2

    else:
        raise ValueError(f'Cannot handle dispersion function of type {ftype}')

    return wave, fields


def read_multispec(fitsfile, reform=True, quiet=True):
    """Read an IRAF spectrum in multispec format from a FITS file

    Args:
        fitsfile (str): Path of the FITS file to read
        reform  (bool): Return flux in to 2D [n, m] instead of 3D [n, 1, m]
        quiet   (bool): Suppress print statements

    Returns:
        The file's header data
        An array of wavelengths dimensioned [NORDERS, NWAVE]
        An array of flux values dimensioned [NCOMPONENTS, NORDERS, NWAVE]
            If NORDERS=1, array is [NCOMPONENTS, NWAVE]; if NCOMPONENTS is also
            unity, array is [NWAVE]. (This can be changed
            using the reform keyword.) Commonly the first dimension
            is 4 and indexes the spectrum, an alternate version of
            the spectrum, the sky, and the error array.  I have also
            seen examples where NCOMPONENTS=2 (probably spectrum and
            error).  Generally I think you can rely on the first element
            flux[0] to be the extracted spectrum.  I don't know of
            any foolproof way to figure out from the IRAF header what the
            various components are.
    """

    fh = pyfits.open(fitsfile)
    try:
        header = fh[0].header
        flux = fh[0].data

    finally:
        fh.close()

    temp = flux.shape
    nwave = temp[-1]
    if len(temp) == 1:
        nspec = 1

    else:
        nspec = temp[-2]

    # first try linear dispersion
    try:
        crval1 = header['crval1']
        crpix1 = header['crpix1']
        cd1_1 = header['cd1_1']
        ctype1 = header['ctype1']
        if ctype1.strip() == 'LINEAR':
            wavelen = np.zeros((nspec, nwave), dtype=float)
            ww = (np.arange(nwave, dtype=float) + 1 - crpix1) * cd1_1 + crval1

            for i in range(nspec):
                wavelen[i, :] = ww

            # handle log spacing too
            dcflag = header.get('dc-flag', 0)
            if dcflag == 1:
                wavelen = 10.0 ** wavelen
                if not quiet:
                    print('Dispersion is linear in log wavelength')

            elif dcflag == 0:
                if not quiet:
                    print('Dispersion is linear')

            else:
                raise ValueError(
                    'Dispersion not linear or log (DC-FLAG=%s)' % dcflag)

            if nspec == 1 and reform:
                # get rid of unity dimensions
                flux = np.squeeze(flux)
                wavelen.shape = (nwave,)

            return header, wavelen, flux

    except KeyError:
        pass

    # get wavelength parameters from multispec keywords
    try:
        wat2 = header['wat2_*']

    except KeyError:
        raise ValueError(
            'Cannot decipher header, need either WAT2_ or CRVAL keywords')

    # concatenate them all together into one big string
    watstr = []
    for i in range(len(wat2)):
        # hack to fix the fact that older pyfits versions (< 3.1)
        # strip trailing blanks from string values in an apparently
        # irrecoverable way
        # v = wat2[i].value
        v = wat2[i]
        v = v + (" " * (68 - len(v)))  # restore trailing blanks
        watstr.append(v)

    watstr = ''.join(watstr)

    # find all the spec#="..." strings
    specstr = [''] * nspec
    for i in range(nspec):
        sname = 'spec' + str(i + 1)
        p1 = watstr.find(sname)
        p2 = watstr.find('"', p1)
        p3 = watstr.find('"', p2 + 1)
        if p1 < 0 or p1 < 0 or p3 < 0:
            raise ValueError('Cannot find {sname} in WAT2_* keyword')

        specstr[i] = watstr[p2 + 1:p3]

    wparms = np.zeros((nspec, 9), dtype=float)
    for i in range(nspec):
        w1 = np.asarray(specstr[i].split(), dtype=float)
        wparms[i, :] = w1[:9]
        if w1[2] == -1:
            raise ValueError(
                f'Spectrum {i + 1} has no wavelength calibration (type={w1[2]})')

            # elif w1[6] != 0:
            #    raise ValueError('Spectrum %d has non-zero redshift (z=%f)' % (i+1,w1[6]))

    wavelen = np.zeros((nspec, nwave), dtype=float)
    wavefields = [None] * nspec
    for i in range(nspec):
        # if i in skipped_orders:
        #    continue
        verbose = (not quiet) and (i == 0)
        if wparms[i, 2] == 0 or wparms[i, 2] == 1:
            # simple linear or log spacing
            wavelen[i, :] = np.arange(nwave, dtype=float) * wparms[i, 4] + wparms[i, 3]
            if wparms[i, 2] == 1:
                wavelen[i, :] = 10.0 ** wavelen[i, :]
                if verbose:
                    print('Dispersion is linear in log wavelength')

            elif verbose:
                print('Dispersion is linear')

        else:
            # non-linear wavelengths
            wavelen[i, :], wavefields[i] = nonlinear_wave(
                nwave, specstr[i], verbose=verbose)

        wavelen *= 1.0 + wparms[i, 6]
        if verbose:
            print(f"Correcting for redshift: z={wparms[i, 6]}")

    if nspec == 1 and reform:
        # get rid of unity dimensions
        flux = np.squeeze(flux)
        wavelen.shape = (nwave,)

    return header, wavelen, flux
