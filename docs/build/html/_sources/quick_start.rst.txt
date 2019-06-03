Quick Start
===========

.. note::
   The following is provided as a simple demonstration on how to use
   **SNData**. For more information, or for usage instructions on a specific
   module, please see that module's documentation page.

Importing a Survey
------------------

To access data from a specific survey, simply import it from the parent
package. For demonstration purposes we will be using the third data release
from the Carnegie Supernova Survey.

.. code-block:: python
   :linenos:

    from SNData.csp import dr3

    # The type of data in this release
    print(dr3.data_type)

    # The primary publication(s) and NASA ADS link(s) describing the data
    print(dr3.publication)
    print(dr3.ads)


Downloading Data
----------------

To minimize the amount of disk space it uses, **SNData** does not come
pre-installed with data from any survey. Instead, users must manually tell
**SNData** to download (or delete) data from the local machine.

.. code-block:: python
   :linenos:

    # Get an overview of the provided data
    help(dr3)

    # Check for available data
    print(dr3.data_is_available())

    # Download data for the given survey / data release
    dr3.download_module_data()

    # Delete any downloaded data for the given survey / data release
    dr3.delete_module_data()


It is useful to note that any data has already been downloaded is skipped over
by ``download_module_data``, making it safe to call in an automated pipeline
environment.

Accessing Data
--------------

Observational data can be retrieved for individual objects as astropy tables.
The ``iter_data`` function is also provided for convenience to iterate over
data for all available objects.

.. code-block:: python
   :linenos:

    # Get a list of available objects
    list_of_ids = dr3.get_available_ids()

    # Get data for a given object
    demo_id = list_of_ids[0]
    data_table = get_data_for_id(demo_id)
    print(data_table)

    # Don't forget to check the meta data
    print(data_table.meta)

    for data in dr3.iter_data():
        print(data)
        break

Integration with Vizier
-----------------------

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

.. _Vizier.com: https://vizier.unistra.fr


Integration with SNCosmo
------------------------

**SNData** supports the formatting of data from photometric surveys for use
with the `SNCosmo`_ light-curve fitter. This includes registering the filter
transmission curves for a given survey.

.. code-block:: python
   :linenos:

    import sncosmo

    # The names of the bands that will be registered
    print(dr3.band_names)

    # Register the band-passes
    dr3.register_filters()

    # Get data for a given object (``demo_id`` defined in a previous example)
    data_table = dr3.get_sncosmo_input(demo_id)
    print(data_table)

    # You can also iterate over all data tables
    for data in dr3.iter_data(format_sncosmo=True):
        print(data)
        break

.. warning::
  The ``get_sncosmo_input`` function is only available for surveys that provide
  photometric data. For example, it is not available in ``SNData.csp.dr1``.


.. _SNCosmo: https://sncosmo.readthedocs.io/en/v1.8.x/