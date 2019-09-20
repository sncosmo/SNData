Integrated Services
===================

**SNData** provides a handful of utilities for interfacing with external
services commonly used in the astronomical and supernova sciences.


Vizier
------

If publication for a given data set includes tables available on `Vizier.com`_,
these tables are accessible via their table numbers in the publication. Any
table descriptions provided by Vizier are also included with the table as
metadata.

.. code-block:: python
   :linenos:

    from sndata.sdss import sako18

    # A list of available table numbers
    table_nums = dr3.get_available_tables()

    table = dr3.load_table(table_nums[0])
    print(table.meta)
    print(table)

Publications will often reference data tables that were not included in the
publication, but are available online. These tables may also included in
``get_available_tables``, but will have a string identifier instead of an
integer table number. An example of this is the SDSS SNe data release from
Sako et al. 2018 which contained a summary table they call the "master" table

.. code-block:: python
   :linenos:

    from sndata.sdss import sako18
    sako18.download_module_data()
    print(sako18.get_available_tables())

    >>> ['master']

SNCosmo
-------

**SNData** is automatically formats data for use with the `SNCosmo`_
light-curve fitter. To fully take advantage of this, **SNData** is also able to
register the filter transmission curves for a given survey into the `sncosmo`
registry (the registry is how sncosmo keeps track of what various filters,
models, etc. are called).

.. code-block:: python
   :linenos:

    import sncosmo

    # The names of the bands that will be registered
    print(dr3.band_names)

    # Register the band-passes of the survey with SNCosmo
    # You can optionally specify ``force=True`` to re-register band-passes
    dr3.register_filters()

    # Get data for SN 2004dt
    data_table = dr3.get_data_for_id('2004dt')
    print(data_table)

    # Fit the data
    model = sncosmo.Model('salt2')
    model.set(z=data_table.meta['redshift'])
    result, fitted_model = sncosmo.fit_lc(
        data=data_table,
        model=model,
        vparam_names=['t0', 'x0', 'x1', 'c'])

    print(result)


NASA/IPAC Extragalactic Database (NED)
--------------------------------------

The `NED`_ is a comprehensive database of extragalactic objects maintained by
NASA. You can query NED for the position (RA and Dec) of `IAU`_ registered
supernovae using the ``query_ned_coords`` function.

.. code-block:: python
   :linenos:

    from sndata import query_ned_coords

    ra, dec = query_ned_coords('2011fe')
    print(f'RA: {ra}, DEC: {dec}')


Open Supernova Catalog (OSC)
----------------------------

The `OSC`_ is a centralized, open source repository for SN metadata,
light-curves, and spectra. All three of these data types can be queried using
**SNData**.

.. code-block:: python
   :linenos:

    from sndata import query_osc, query_osc_photometry, query_osc_spectra

    object_name = '2011fe'

    # Object meta data
    print(query_osc(object_name))

    # All available photometric data as an astropy table
    data_table = query_osc_photometry(object_name)
    print(data_table)

    # Note that photometric data includes the meta data
    print(data_table.meta)

    # Finally, spectral data can also be retrieved as a list of dictionaries
    print(query_osc_spectra(object_name))


.. _Vizier.com: https://vizier.unistra.fr
.. _SNCosmo: https://sncosmo.readthedocs.io/en/v1.8.x/
.. _NED: https://ned.ipac.caltech.edu
.. _IAU: https://www.iau.org/public/themes/naming_stars/
.. _OSC: https://sne.space
