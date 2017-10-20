
Installation
============

This section describes how to obtain the source code and carry out basic tests
to make sure your system has been set up correctly and all dependencies are
fulfilled.

Getting the code
----------------

The code for the client library is hosted at
https://github.com/gpodder/mygpoclient/. You can download the latest version of
the code by using the command:

.. code-block:: bash

 	git clone https://github.com/gpodder/mygpoclient.git

or install it with ``pip``:

.. code-block:: bash

 	pip install mygpoclient


Running Unit tests
------------------

To make sure that the library is working and all dependencies are installed,
please install the dependencies listed in the `DEPENDENCIES
<https://github.com/gpodder/mygpoclient/blob/master/DEPENDENCIES>`_ file.
After that, you can easily run the unit tests that come with the library:

.. code-block:: bash

	make test

This will run all unit tests and doctests in the library. After the tests have
been completed, you should get a summary with the test and code coverage
statistics. The output should look like the following example if everything
works (please note that the statement count could be different as development
of the library continues):

.. code-block:: bash

	Name                  Stmts   Exec  Cover   Missing
	---------------------------------------------------
	mygpoclient               5      5   100%
	mygpoclient.api         155    155   100%
	mygpoclient.http         52     52   100%
	mygpoclient.json         22     22   100%
	mygpoclient.locator      52     52   100%
	mygpoclient.simple       16     16   100%
	mygpoclient.util         20     20   100%
	---------------------------------------------------
	TOTAL                   322    322   100%
	---------------------------------------------------
	Ran 81 tests in 4.987s


Reading the module documentation
--------------------------------

You can use the ``pydoc`` utility to read the documentation for the library.
You probably want to use the following commands:


.. code-block:: bash

	pydoc mygpoclient.simple
 	pydoc mygpoclient.api

If you want, you can let Epydoc create the API documentation in the source
tree:

.. code-block:: bash

	make docs

The resulting documentation will be created in the ``docs/``
subdirectory.
