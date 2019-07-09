Quick Start
===========

The following is provided as a simple demonstration on how to use **SNData**.
For more information, or for usage instructions on a specific module, please
see that module's documentation page.

Importing a Survey
------------------

To access data from a specific survey, simply import it from the parent
package. A summary of each data release, including any deviations from the
standard UI, can be accessed by calling the builtin ``help`` function. For
demonstration purposes we will be using the third data release from the
Carnegie Supernova Survey.

.. code-block:: python
   :linenos:

    from SNData.csp import dr3

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

The ``iter_data`` allows users to optionally select a subset of the total data
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

.. important:: In order to evaluate a filter function, the `iter_data` needs to
   read data for a given object from file. For this reason, filter functions
   should not be used in an attempt improve runtime by reducing I/O operations
   as it will have no effect.
