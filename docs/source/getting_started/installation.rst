Installation and Setup
======================

To install the package, please choose from one of the options below.

.. note::
   No survey data is downloaded when installing or upgrading **SNData**.
   All data management is handled explicitly, as outlined in the
   `Slow Start <slow_start.html>`_ tutorial.

Using PIP (Recommended)
-----------------------

To install using the `pip package manager`_, run:

.. code-block:: bash

    pip install sndata

Pip will automatically install any missing dependencies in your Python
environment. If you have any issues installing the package, try installing the
dependencies manually and then reinstall **sndata**.

A list of required dependencies is provided on GitHub via a
``requirements.txt`` document. Dependencies can be installed by running:

.. code-block:: bash

    # Clone the source code from GitHub
    git clone http://github.com/djperrefort/SNData SNData

    # Install dependencies
    pip install -r SNData/requirements.txt

Using setup.py
--------------

If pip is unavailable on your system, the package source code is
available on `GitHub`_.

.. code-block:: bash

    # Clone the source code from GitHub
    git clone http://github.com/djperrefort/SNData SNData

    # Install the package from source
    cd SNData
    python setup.py install --user

As in the previous method, any missing dependencies in your Python environment
should be installed automatically. If you have any issues installing the
package, install each dependency from ``requirements.txt`` and then try again.

.. _pip package manager: https://pip.pypa.io/en/stable/
.. _GitHub: https://github.com/djperrefort/sndata

Configuring Data Storage
------------------------

By default data downloaded by **sndata** is stored in the installation directory.
This can be changed to a custom directory by specifying the value `SNDATA_DIR`
in your environment (i.e., in you `.bash_profile` or `.bashrc` file).
For example:

.. code-block:: bash

    export SNDATA_DIR="/your/data/directory/path"
