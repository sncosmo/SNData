Slow Start
==========

The following is provided's a simple demonstration of the various functionality
available in **SNData**. For more information, or for usage instructions on a
specific module, please see that module's documentation page.

Importing a Survey
------------------

To access data from a specific survey, simply import it from the parent
package. A summary of each data release, including any deviations from the
standard UI, can be accessed by calling the builtin ``help`` function. For
demonstration purposes we will be using the third data release from the
Carnegie Supernova Survey.

.. code-block:: python
   :linenos:

   from sndata.csp import dr3

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

Accessing Data
--------------

Observational data can be retrieved for individual objects as astropy tables.

.. code-block:: python
   :linenos:

   # Get a list of available objects
   list_of_ids = dr3.get_available_ids()

   # Get data for a given object
   demo_id = list_of_ids[0]
   data_table = get_data_for_id(demo_id)
   print(data_table)

.. important:: Data tables returned by SNDATA are formatted for use with the
   ``sncosmo`` python package. In doing so, the values of the table may be
   manipulated from the original file data into different units, column names,
   etc. To disable this feature, specify the ``format_table=False`` argument.

The ``iter_data`` function is also provided for convenience to iterate over
data for all available objects.

   # Don't forget to check the meta data
   print(data_table.meta)

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
       return data_table.meta['redshift'] < .1

   for data in dr3.iter_data(filter_func=filter_func):
       print(data)
       break

.. important:: As ``iter_data`` iterates over supernovae, it reads in data
   from file for a given object before checking the filter function. For this
   reason, filter functions should not be used in an attempt improve runtime
   by reducing I/O operations as it will have no effect.

Data Formatting
---------------

**SNData** is automatically formats data for use with the `SNCosmo`_
light-curve fitter. To fully take advantage of this, **SNData** is also able to
register the filter transmission curves for a given survey into the `sncosmo`
registry (the registry is how sncosmo keeps track of what various filters,
models, etc. are called).

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
   model.set(z=data_table.meta['redshift'])
   result, fitted_model = sncosmo.fit_lc(
       data=data_table,
       model=model,
       vparam_names=['t0', 'x0', 'x1', 'c'])

   print(result)
