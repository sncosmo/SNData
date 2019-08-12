Equation of State: Supernovae trace Cosmic Expansion (ESSENCE)
==============================================================

.. automodule:: sndata.essence

+---------------------+-------------+---------------+-----------------------------+
| Data Release        | Module Name | Data Type     | Publication                 |
+=====================+=============+===============+=============================+
| Narayan et al. 2016 | narayan16   | photometric   | `Narayan et al. (2016)`_    |
+---------------------+-------------+---------------+-----------------------------+

.. Matheson module not fully integrated
 | Matheson et a. 2005 | matheson05  | Spectroscopic | `Matheson et al. (2005)`_   |
 +---------------------+-------------+---------------+-----------------------------+

.. _Matheson et al. (2005): https://ui.adsabs.harvard.edu/abs/2005AJ....129.2352M/abstract
.. _Narayan et al. (2016): https://ui.adsabs.harvard.edu/abs/2016ApJS..224....3N/abstract

.. Matheson module not fully integrated
   Matheson et al. 2005
   --------------------

   .. automodule:: sndata.essence.matheson05

   .. py:currentmodule:: sndata.essence.matheson05

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


Narayan et al. 2016
-------------------

.. automodule:: sndata.essence.narayan16

.. py:currentmodule:: sndata.essence.narayan16

Attribute Summaries
^^^^^^^^^^^^^^^^^^^

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

Function Documentation
^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: delete_module_data
.. autofunction:: download_module_data
.. autofunction:: get_available_ids
.. autofunction:: get_available_tables
.. autofunction:: get_data_for_id
.. autofunction:: iter_data
.. autofunction:: load_table
.. autofunction:: register_filters
