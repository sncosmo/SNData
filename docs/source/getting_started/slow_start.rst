.. _SlowStart:

Slow Start
==========

The following is provided as an in depth demonstration of the various
functionality available in **SNData**. For more information on a specific
module, please see that module's page in the API documentation.

Importing a Survey
------------------

To access data from a specific survey, import it from the parent package. A
summary of each data release, including any deviations from the standard UI,
can be accessed by calling the builtin ``help`` function. For demonstration
purposes we will be using the third data release from the Carnegie Supernova
Project.

.. code-block:: python
   :linenos:

   from sndata.csp import DR3

   # At instantiation, the DR3 class determines where the data
   # is located on your machine
   dr3 = DR3()

   # Information about the parent survey
   print(dr3.survey_name)
   print(dr3.survey_abbrev)

   # A summary of the DR3 data set
   help(dr3)

   # Where to go for more information
   print(dr3.survey_url)

   # The type of data in this release
   print(dr3.data_type)

   # The primary publication(s) and NASA ADS link(s) describing the data
   print(dr3.publications)
   print(dr3.ads_url)

   # Photometric data releases include filters
   print(dr3.band_names)


Downloading Data
----------------

To minimize disk space usage, **SNData** does not come pre-installed with any
survey data. Instead, users must manually tell **SNData** to download
(or delete) data from their local machine.

.. code-block:: python
   :linenos:

   # Get an overview of the provided data
   help(dr3)

   # Download data for the given survey / data release
   dr3.download_module_data()

   # Delete any downloaded data for the given survey / data release
   dr3.delete_module_data()


It is useful to note that any data has already been downloaded is skipped over
by ``download_module_data``, making it safe to call in an automated pipeline
environment. This behavior can be disabled by specifying the ``force=True``
argument.

.. Important:: Survey data is often hosted across multiple websites. As such,
it is possible the server responsible for hosting a subset of a survey's
data (e.g. the filter transmission curves) is temporarily offline. In this
case **SNData** will raise a warning and continue downloading any data that is
still online. The ``download_module_data`` function can then be re-run once
the server is back online.


Accessing Data
--------------

Observational data can be retrieved for individual objects as astropy tables.
For convenience, the Ra, Dec, redshift, and redshift error are included in the
table's meta data when available.

.. code-block:: python
   :linenos:

   # Get a list of available objects
   list_of_ids = dr3.get_available_ids()

   # Get data for a given object
   demo_id = list_of_ids[0]
   data_table = dr3.get_data_for_id(demo_id)
   print(data_table)

   # Don't forget to check the meta data!
   print(data_table.meta)

Data tables returned by SNData are formatted for use with the ``sncosmo``
python package. In doing so, the values of the table may be manipulated from
the original file data into different units, column names, etc. To disable
this feature, specify the ``format_table=False`` argument.

The ``iter_data`` function is also provided for convenience to iterate over
data for all available objects.

.. code-block:: python
   :linenos:

   for data in dr3.iter_data():
       print(data)
       break

This function allows users to optionally select a subset of the total data
by defining a filter function. This function should accept a data table
yielded by ``iter_data`` and return a boolean. For example, to only select
target with a redshift less than .1:

.. code-block:: python
   :linenos:

   def filter_func(data_table):
       return data_table.meta['z'] < .1

   for data in dr3.iter_data(filter_func=filter_func):
       print(data)
       break

.. important:: As ``iter_data`` iterates over supernovae, it reads in data
   from file for a given object before checking the filter function. For this
   reason, filter functions should not be used in an attempt improve runtime
   by reducing I/O operations as it will have no effect.


Reading Tables
--------------

Some surveys include summary tables in their data releases. The inclusion of
tables from published papers is also common.

.. code-block:: python
   :linenos:

   # Check what tables are available
   published_tables = dr3.get_available_tables()
   print(published_tables)

   # Read one of those tables by referencing the table name or number
   demo_table_name = published_tables[0]
   demo_table = dr3.load_table(demo_table_name)


Note that the ``load_table`` function caches the returned result in memory.
This improves the speed of successive calls and means you don't have to be
worried about I/O performance.


Registering Filters with SNCosmo
--------------------------------

**SNData** automatically formats data for use with the `SNCosmo`_ package.
To fully take advantage of this, **SNData** is also able to register the
filter transmission curves for a given survey into the `sncosmo` registry
(the registry is how SNCosmo keeps track of what each filter, model, etc.
are called).

.. _SNCosmo: https://sncosmo.readthedocs.io/en/v1.8.x/

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
   model.set(z=data_table.meta['z'])
   result, fitted_model = sncosmo.fit_lc(
       data=data_table,
       model=model,
       vparam_names=['t0', 'x0', 'x1', 'c'])

   print(result)
