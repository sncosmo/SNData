SNData
======

.. |python| image:: https://img.shields.io/badge/python-3.6+-blue.svg
    :target: #

.. |license| image:: https://img.shields.io/badge/license-GPL%20v3.0-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html

.. |travis| image:: https://www.travis-ci.com/mwvgroup/SNData.svg?branch=master
   :target: https://www.travis-ci.com/mwvgroup/SNData

.. |cover| image:: https://coveralls.io/repos/github/mwvgroup/SNData/badge.svg?branch=master
   :target: https://coveralls.io/github/mwvgroup/SNData?branch=master

.. |docs| image:: https://readthedocs.org/projects/sn-data/badge/?version=latest
   :target: https://sn-data.readthedocs.io/en/latest/?badge=latest

.. rst-class:: badges

   +--------------------------------------------+
   | |python| |license| |travis| |cover| |docs| |
   +--------------------------------------------+


**SNData** provides access to spectroscopic and photometric data published by
a variety of supernova (SN) surveys. It is designed to support the development
of scalable analysis pipelines that translate with minimal effort between
different data sets or to a combination of multiple data sets. A summary of
accessible data sets is provided below. Access to additional surveys is added
upon request or as needed for individual research projects undertaken by the
developer(s). To request an additional survey / data release, please raise an
issue on `GitHub`_.

.. _GitHub: https://github.com/djperrefort/sndata


Using These Docs
----------------

**SNData** is designed to provide as consistent of an interface as possible
across surveys. The *Getting Started* guides are intended to help you get up
and running quickly and to familiarize you with the general **SNData**
interface. Additional API documentation is provided for each individual
data set to highlight any (very) minor deviations a particular survey or
data release may have from the rest of the package. In general you should:

1. Read the installation guide (~1 minute if you know how to use ``pip``)
2. Read the quick start guide to learn how the package works (~5 minutes)
3. Read the slow start guide for a better understanding of the available features and how they can make your life easier (~10 minutes)
4. Refer to the API documentation for a given survey as you see necessary


Available Data
--------------

+------------------------------------------------------+---------------+--------------------------+
| Survey Name                                          | Data Type     | Data Release             |
+======================================================+===============+==========================+
|                                                      | Spectroscopic | `DR1`_                   |
+ Carnegie Supernova Project                           +---------------+--------------------------+
|                                                      | Photometric   | `DR3`_                   |
+------------------------------------------------------+---------------+--------------------------+
| Dark Energy Survey                                   | Photometric   | `SN3YR`_                 |
+------------------------------------------------------+---------------+--------------------------+
+ Equation of State: Supernovae Trace Cosmic Expansion | Photometric   | `Narayan et al. 2016`_   |
+------------------------------------------------------+---------------+--------------------------+
+ Joint Light-Curve Analysis                           | Photometric   | `Betoule et al. (2014)`_ |
+------------------------------------------------------+---------------+--------------------------+
|                                                      | Photometric   | `Sako et al. 2018`_      |
+ Sloan Digital Sky Survey                             +---------------+--------------------------+
|                                                      | Spectroscopic | `Sako et al. 2018`_      |
+------------------------------------------------------+---------------+--------------------------+

.. _DR1: https://csp.obs.carnegiescience.edu/news-items/CSP_spectra_DR1
.. _DR3: https://csp.obs.carnegiescience.edu/news-items/csp-dr3-photometry-released
.. _SN3YR: https://des.ncsa.illinois.edu/releases/sn
.. _Narayan et al. 2016: http://www.ctio.noao.edu/essence/
.. _Betoule et al. (2014): https://ui.adsabs.harvard.edu/abs/2014A%26A...568A..22B/abstract
.. _Sako et al. 2018: http://data.darkenergysurvey.org/sdsssn/dataRelease/


.. toctree::
   :hidden:
   :maxdepth: 0

   Overview<self>

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Getting Started:

   getting_started/installation
   getting_started/quick_start
   getting_started/slow_start
   getting_started/combining_datasets

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Module API Docs:

   module_docs/sndata
   module_docs/csp
   module_docs/des
   module_docs/essence
   module_docs/jla
   module_docs/sdss
