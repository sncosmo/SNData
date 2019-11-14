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
data release may have from the rest of the package.


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
   getting_started/installation
   getting_started/quick_start
   getting_started/combining_datasets

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Module API Docs:

   module_docs/sndata
   module_docs/csp
   module_docs/des
   module_docs/essence
   module_docs/sdss
