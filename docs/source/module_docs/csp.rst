Carnegie Supernova Project (CSP)
================================

.. automodule:: SNData.csp

+--------------+---------------+---------------+-----------------------------+
| Data Release | Module Name   | Data Type     | Publication                 |
+==============+===============+===============+=============================+
| DR1          | csp.dr1       | Spectroscopic | `Folatelli et al. (2013)`_  |
+--------------+---------------+---------------+-----------------------------+
| DR3          | csp.dr3       | Photometric   | `Krisciunas et al. (2017)`_ |
+--------------+---------------+---------------+-----------------------------+

.. _Folatelli et al. (2013): https://ui.adsabs.harvard.edu/abs/2013ApJ...773...53F/abstract
.. _Krisciunas et al. (2017): https://ui.adsabs.harvard.edu/abs/2017AJ....154..211K/abstract


Data Release 1
--------------

.. automodule:: SNData.csp.dr1

.. py:currentmodule:: SNData.csp.dr1

**Attribute Summaries:**

.. autosummary::

    delete_module_data
    download_module_data
    get_available_ids
    get_available_tables
    get_data_for_id
    iter_data
    load_table

**Function Documentation:**

.. autofunction:: delete_module_data
.. autofunction:: download_module_data
.. autofunction:: get_available_ids
.. autofunction:: get_available_tables
.. autofunction:: get_data_for_id
.. autofunction:: iter_data
.. autofunction:: load_table


Data Release 3
--------------

.. automodule:: SNData.csp.dr3

.. py:currentmodule:: SNData.csp.dr3

**Attribute Summaries:**

.. autosummary::

    delete_module_data
    download_module_data
    get_available_ids
    get_available_tables
    get_data_for_id
    iter_data
    load_table
    register_filters
    band_names

**Function Documentation:**

.. autofunction:: delete_module_data
.. autofunction:: download_module_data
.. autofunction:: get_available_ids
.. autofunction:: get_available_tables
.. autofunction:: get_data_for_id
.. autofunction:: iter_data
.. autofunction:: load_table
.. autofunction:: register_filters
