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
