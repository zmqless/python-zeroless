.. _development:

Development
===========

This page describes Zeroless development process and contains general
guidelines and information on how to contribute to the project.

Contributing
------------

We welcome contributions of any kind (ideas, code, tests, documentation,
examples, ...).

General Contribution Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Any non-trivial change must contain tests.
* All the functions and methods must contain Sphinx docstrings which are
  used to generate the API documentation.
* If you are adding a new feature, make sure to add a corresponding
  documentation.

Code Style Guide
~~~~~~~~~~~~~~~~

* We follow `PEP8 Python Style Guide`_.
* Use 4 spaces for a tab.
* Use 79 characters in a line.
* Make sure edited file doesn't contain any trailing whitespace.

.. _`PEP8 Python Style Guide`: http://www.python.org/dev/peps/pep-0008/

Testing
-------

Tests make use of the ``py.test`` framework and are located in the tests/
folder. However, we recommend the usage of ``tox`` as it will test our
codebase against both Python 2.7 and 3.0.

.. include:: ../README.rst
   :start-after: _testing_content_start:
   :end-before:  _testing_content_end:

All functionality (including new features and bug fixes) must include a
test case to check that it works as expected, so please include tests
for your patches if you want them to get accepted sooner.
