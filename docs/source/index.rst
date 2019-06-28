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

+----------------------------+------------------+---------------+-----------------------------------------------------------------------------------------------------------------+
| Survey Name                | Data Release     | Data Type     | External Link                                                                                                   |
+============================+==================+===============+=================================================================================================================+
|                            | DR1              | Spectroscopic | `csp.obs.carnegiescience.edu <https://csp.obs.carnegiescience.edu/news-items/CSP_spectra_DR1>`_                 |
+ Carnegie Supernova Project +------------------+---------------+-----------------------------------------------------------------------------------------------------------------+
|                            | DR3              | Photometric   | `csp.obs.carnegiescience.edu <https://csp.obs.carnegiescience.edu/news-items/csp-dr3-photometry-released>`_     |
+----------------------------+------------------+---------------+-----------------------------------------------------------------------------------------------------------------+
| Dark Energy Survey         | SN3YR            | Photometric   | `des.ncsa.illinois.edu <https://des.ncsa.illinois.edu/releases/sn>`_                                            |
+----------------------------+------------------+---------------+-----------------------------------------------------------------------------------------------------------------+
| Sloan Digital Sky Survey   | Sako et al. 2018 | Photometric   | `data.darkenergysurvey.org <http://data.darkenergysurvey.org/sdsssn/dataRelease/>`_                             |
+----------------------------+------------------+---------------+-----------------------------------------------------------------------------------------------------------------+

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Getting Started:

   Overview<self>
   installation
   quick_start
   integrated_services

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Module Docs:

   csp
   des
   sdss
