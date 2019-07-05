SNData
======

**SNData** provides a uniform Python interface for data releases published by
various supernova surveys. A summary of available data sets is provided below.
Access to additional surveys is added upon request or as needed for individual
research projects undertaken by the developer(s). To request an additional
survey / data release, please raise an issue on `GitHub`_.

.. _GitHub: https://github.com/djperrefort/sndata


Using These Docs
----------------

**SNData** is designed to provide as consistent of an interface as possible
across surveys. However, this is not always possible as the data products
made available by different surveys can vary wildly in their format. The
`Installation <installation.html>`_ and `Quick Start <quick_start.html>`_
guides are intended to help you get up and running quickly and to familiarize
you with the general **SNData** interface. Additional documentation is
provided for each individual dataset to highlight any minor deviations a
particular survey or data release may have from the rest of the package.


Available Data
--------------

+------------------------------------------------------+------------------------+---------------+
| Survey Name                                          | Data Release           | Data Type     |
+======================================================+========================+===============+
|                                                      | `DR1`_                 | Spectroscopic |
+ Carnegie Supernova Project                           +------------------------+---------------+
|                                                      | `DR3`_                 | Photometric   |
+------------------------------------------------------+------------------------+---------------+
| Dark Energy Survey                                   | `SN3YR`_               | Photometric   |
+------------------------------------------------------+------------------------+---------------+
+ Equation of State: Supernovae Trace Cosmic Expansion | `Narayan et al. 2016`_ | Photometric   |
+------------------------------------------------------+------------------------+---------------+
| Sloan Digital Sky Survey                             | `Sako et al. 2018`_    | Photometric   |
+------------------------------------------------------+------------------------+---------------+

.. _DR1: https://csp.obs.carnegiescience.edu/news-items/CSP_spectra_DR1
.. _DR3: https://csp.obs.carnegiescience.edu/news-items/csp-dr3-photometry-released
.. _SN3YR: https://des.ncsa.illinois.edu/releases/sn
.. _Narayan et al. 2016: http://www.ctio.noao.edu/essence/
.. _Sako et al. 2018: http://data.darkenergysurvey.org/sdsssn/dataRelease/


.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Getting Started:

   Overview<self>
   installation
   quick_start
   integrated_services
   .. combining_datasets

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Module API Docs:

   module_docs/combined
   module_docs/csp
   module_docs/des
   module_docs/essence
   module_docs/sdss
