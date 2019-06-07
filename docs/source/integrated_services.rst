Integrated Services
===================

Vizier
------

If publication for a given data set includes tables available on `Vizier.com`_,
these tables are accessible via their table numbers in the publication.

.. code-block:: python
   :linenos:

    # A list of available table numbers
    table_nums = dr3.get_available_tables()

    table = dr3.load_table(table_nums[0])
    print(table)

.. note::
   Publications will often reference data tables that were not included in the
   publication, but are available online. These tables are also included in
   ``get_available_tables``, but will have a string identifier instead of an
   integer.


SNCosmo
-------

**SNData** supports the formatting of data from photometric surveys for use
with the `SNCosmo`_ light-curve fitter. This includes registering the filter
transmission curves for a given survey.

.. code-block:: python
   :linenos:

    import sncosmo

    # The names of the bands that will be registered
    print(dr3.band_names)

    # Register the band-passes of the survey with SNCosmo
    # You can optionally specify ``force=True`` to re-register band-passes
    dr3.register_filters()

    # Get data for a given object (``demo_id`` defined in a previous example)
    data_table = dr3.get_sncosmo_input(demo_id)
    print(data_table)

    # You can also iterate over all data tables
    for data in dr3.iter_data(format_sncosmo=True):
        print(data)
        break

.. warning::
  The ``get_sncosmo_input`` function is intended for use with surveys that
  provide photometric data. When called for surveys without photometric data
  (such as ``SNData.csp.dr1``) the function will raise an error.


SNooPy
------

`SNooPy`_ is a collection of Python tools developed by the Carnegie Supernova
Project for the analysis of TypeIa supernovae. **SNData** provides the
``parse_snoopy_data`` for parsing snoopy files as an astropy table.

.. code-block:: python
   :linenos:

    from SNData import parse_snoopy_data

    data_table = parse_snoopy_data('my_directory/my_file.snpy')


NASA/IPAC Extragalactic Database (NED)
--------------------------------------

The `NED`_ is a comprehensive database of data for extragalactic objects
maintained by NASA. Your can query NED for the position (RA and Dec) of `IAU`_
registered supernovae using the ``query_ned_coords`` function.

.. code-block:: python
   :linenos:

    from SNData import query_ned_coords

    ra, dec = query_ned_coords('2011fe')
    print(f'RA: {ra}, DEC: {dec}')



Open Supernova Catalog (OSC)
----------------------------

The `OSC`_ is a centralized, open source repository for SN metadata,
light-curves, and spectra. All three of these data types can be quiered using
**SNData**.

.. code-block:: python
   :linenos:

    from SNData import query_osc, query_osc_photometry, query_osc_spectra

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
.. _SNooPy: https://csp.obs.carnegiescience.edu/data/snpy
.. _NED: https://ned.ipac.caltech.edu
.. _IAU: https://www.iau.org/public/themes/naming_stars/
.. _OSC: https://sne.space
