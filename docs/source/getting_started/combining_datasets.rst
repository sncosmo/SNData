Combining Data Sets
===================

**SNData** allows users to combine data sets into a single ``CombinedDataset``
object. The resulting object provides the same user interface as a single data
access module (plus a few extra features) but provides access to data from
multiple surveys / data releases.

For demonstration purposes, we demonstrate combining data from the third data
release of the Carnegie Supernova Project and the three year cosmology release
of the Dark Energy Survey.

Creating a Combined Data Set
----------------------------

To create a combined data set, import the data access modules for each of the
data releases you want to join and pass them to the ``CombinedDataset``
object.

.. code-block:: python
   :linenos:

    from SNData import CombinedDataset, csp, des

    combined_data = CombinedDataset(csp.dr3, des.sn3yr)

The resulting object provides the same user interface as the rest of the
**SNData** package, including having the same method names:
