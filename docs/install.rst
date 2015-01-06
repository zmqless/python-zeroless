.. _install:

Install Guide
=============

Install stable releases of Zeroless with ``pip``.

.. include:: ../README.rst
   :start-after: _install_content_start:
   :end-before:  _install_content_end:

.. _install_dependencies:

Dependencies
------------

Zeroless only dependency is PyZMQ_.

.. _install_from_github:

Installing from Github
----------------------

The canonical repository for Zeroless is on GitHub_. 

.. code-block:: bash

    $ git clone git@github.com:zmqless/zeroless.git
    $ cd zeroless
    $ python setup.py develop

The best reason to install from source is to help us develop Zeroless. See the
:doc:`development` section for more on that.

.. _PyZMQ: https://www.github.com/zeromq/pyzmq
.. _GitHub: https://github.com/zmqless/zeroless 
