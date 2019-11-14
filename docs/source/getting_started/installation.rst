Installation and Setup
======================

To install the package, please choose from one of the options below.

.. note::
   No survey data is downloaded when installing or upgrading **SNData**.
   All data management is handled explicitly, as outlined in the
   `Quick Start <quick_start.html>`_ tutorial.

Using PIP (Recommended)
-----------------------

To install using the `pip package manager`_, run:

.. code-block:: bash
   :linenos:

    $ pip install sndata

Pip will automatically install any missing dependencies in your Python
environment. If you have any issues installing the package, try installing the
dependency manually and then reinstall **sndata**. Dependencies can be
installed with pip by running:

.. code-block:: bash
   :linenos:

    $ git clone http://github.com/djperrefort/SNData
    $ cd SNData
    $ pip install -r requirements.txt


Using setup.py
--------------

If pip is unavailable on your system, the package source code is
available on `GitHub`_.

.. code-block:: bash
   :linenos:

    $ git clone http://github.com/djperrefort/SNData
    $ cd SNData
    $ python setup.py install --user

As in the previous method, any missing dependencies in your Python environment
should be installed automatically. If you have any issues installing the
package, install each dependency from ``requirements.txt`` and then try again.

.. _pip package manager: https://pip.pypa.io/en/stable/
.. _GitHub: https://github.com/djperrefort/sndata
