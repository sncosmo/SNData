Combining Data Sets
===================

**SNData** allows users to combine individual data releases into a single
``CombinedDataset`` object. The resulting object provides the same general user
interface as a single data access module but provides access to data from
multiple surveys / data releases.

For demonstration purposes we combine data from the third data
release of the Carnegie Supernova Project and the three year cosmology release
of the Dark Energy Survey.

Creating a Combined Data Set
----------------------------

To create a combined data set, import the data access modules for each of the
data releases you want to join and pass them to the ``CombinedDataset``
object.

.. code-block:: python
   :linenos:

    from sndata import CombinedDataset, csp, des

    combined_data = CombinedDataset(csp.DR3(), des.SN3YR())


The resulting object provides the same user interface as the rest of the
**SNData** package, including having the same method names:

.. code-block:: python
   :linenos:

    # Download all data for the combined data releases
    combined_data.download_module_data()

    # Get a list of available objects
    list_of_ids = combined_data.get_available_ids()

    # Get data for a single object
    demo_id = list_of_ids[0]
    data_table = combined_data.get_data_for_id(demo_id)
    print(data_table)

    # Iterate over data for all objects in the combined data set
    for data in combined_data.iter_data():
        print(data)
        break


.. important::

  Unlike the rest of the **SNData** package, object ID's for a combined data
  set are tuples instead of strings. Each tuple contains three elements
  including (in order) the survey name, data release name, and individual
  object identifier. For example, the ID value for supernova 2007S from CSP
  Data Release 3 would be ``('csp', 'dr3', '2007S')``


Joining Object IDs
------------------

It is possible for two different photometric surveys to observe the same
astronomical object. In this case, object IDs from different surveys can be
"joined" together so that when requesting data for an object data is
returned for all IDs that have been joined together. Accomplishing this is as
simple as:

.. code-block:: python
   :linenos:

   # Note that you can join an arbitrary number of object IDs
   combined_data.join_ids(obj_id_1, obj_id_2, obj_id_3, ...)

   # You can also retrieve a list of joined ID values
   print(combined_data.get_joined_ids())

   # To undo the above joining action
   combined_data.separate_ids(obj_id_1, obj_id_2, obj_id_3, ...)

When retrieving data for a joined ID, the returned data table is simply the
collective data tables for each joined ID stacked vertically.

.. code-block:: python
   :linenos:

   data = combined_data.get_data_for_id(obj_id_1)
   print(data)

It is worth noting that ``CombinedDataset`` objects are aware of successive
join actions. This means that the following two examples are functionally
equivalent.

.. code-block:: python
   :linenos:

   # You can join multiple IDs at once ...
   combined_data.join_ids(obj_id_1, obj_id_2, obj_id_3)

   # Or join them successively
   combined_data.join_ids(obj_id_1, obj_id_2)
   combined_data.join_ids(obj_id_2, obj_id_3)


Excluded Features
-----------------

There are a handful of meta data features provided for individual data releases
that are not supported for combined data sets. The following attributes
do not exist for ``CombinedDataset`` objects:

- ``get_vailable_tables``
- ``load_tables``

