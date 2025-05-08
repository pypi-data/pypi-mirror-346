Installation
------------

Packages are available at the `Connector/Python download site <http://dev.mysql.com/downloads/connector/python/>`_. For some packaging formats, there are different packages for different versions of Python; choose the one appropriate for the version of Python installed on your system.

Installing Connector/Python with pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the recommended way to install Connector/Python.

Make sure you have a recent `pip <https://pip.pypa.io/>`_ version installed on your system. If your system already has ``pip`` installed, you might need to update it. Or you can use the `standalone pip installer <https://pip.pypa.io/en/latest/installing/#installing-with-get-pip-py>`_.

.. code-block:: bash

    shell> pip install mysqlx-connector-python

Installing Connector/Python on Linux Using the MySQL Yum Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You must have the MySQL Yum repository on your system's repository list. To make sure that your Yum repository is up-to-date, use this command:

.. code-block:: bash

    shell> sudo yum update mysql-community-release

Then install Connector/Python as follows:

.. code-block:: bash

    shell> sudo yum install mysqlx-connector-python

Installing Connector/Python on Linux Using an RPM Package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install a Connector/Python RPM package (denoted here as PACKAGE.rpm), use this command:

.. code-block:: bash

    shell> rpm -i PACKAGE.rpm

Installing Connector/Python on Linux Using a Debian Package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install a Connector/Python Debian package (denoted here as PACKAGE.deb), use this command:

.. code-block:: bash

    shell> dpkg -i PACKAGE.deb

Installing Connector/Python from source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prerequisites
~~~~~~~~~~~~~

As of Connector/Python 2.2.3, source distributions include a C++ Extension, that interfaces with a MySQL server with the X Plugin enabled using Protobuf as data interchange format.

To build Connector/Python C++ Extension for Protobuf, you must satisfy the following prerequisites:

* A C/C++ compiler, such as ``gcc``
* Protobuf C++ (version >= 4.21.1, <= 4.21.12)
* Python development files
* MySQL Connector/C or MySQL Server installed

Installing Connector/Python from source on Unix and Unix-Like Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To install Connector/Python from a tar archive, download the latest version (denoted here as <version>), and execute these commands:

.. code-block:: bash

   shell> tar xzf mysqlx-connector-python-<version>.tar.gz
   shell> cd mysqlx-connector-python-<version>.tar.gz
   shell> python setup.py install --with-protobuf-include-dir=<protobuf-include-dir> --with-protobuf-lib-dir=<protobuf-lib-dir> --with-protoc=<protoc-binary>

To see all options and commands supported by setup.py, use this command:

.. code-block:: bash

   shell> python setup.py --help
