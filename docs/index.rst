.. _index:

Zeroless
========

|Build Status| |Coverage Status| |Codacy| |PyPi| |Docs| |License|

This documentation contains notes on some important aspects of developing Zeroless
and an overview of Zeroless' API. For information on how to use ØMQ_ in general,
see the many examples in the excellent ØMQGuide_. It can give a better understanding
of when to use each messaging passing pattern available (i.e. request/reply,
publisher/subscriber, push/pull and pair). Also, more complex use cases, that require
the composition of these patterns, are explained in further details.

Zeroless works with Python 3 (≥ 3.0), and Python 2 (≥ 2.7), with no transformations
or 2to3. Finally, please don't hesitate to report zeroless-specific issues to our
Tracker_ on GitHub.

Zeroless x PyZMQ
================

Differing from PyZMQ_, which tries to stay very close to the C++ implementation,
this project aims to make distributed systems employing ØMQ_ as pythonic as
possible.

Being simpler to use, Zeroless doesn't supports all of the fine aspects and features
of PyZMQ_. However, you can expect to find all the message passing patterns you were
accustomed to (i.e. pair, request/reply, publisher/subscriber, push/pull). Despite
that, the only transport available is TCP, as threads are not as efficient in Python
due to the GIL and IPC is unix-only.

Installing
==========

Install stable releases of Zeroless with ``pip``.

.. code-block:: bash

    $ pip install zeroless

See the :doc:`install` for more detail.

Documentation
=============

Contents:

.. toctree::
   :maxdepth: 4

   install
   quickstart
   development

Zeroless API
============

Contents:

.. toctree::
   :maxdepth: 4

   zeroless

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Development
===========

We welcome contributions of any kind (ideas, code, tests, documentation, examples, ...).
See the :doc:`development` section for further details.

Links
=====

* ØMQ_ Home
* The ØMQGuide_
* Zeroless on GitHub_
* Zeroless on PyPy_
* Issue Tracker_

License
=======

.. include:: ../README.rst
   :start-after: _license_content_start:
   :end-before:  _license_content_end:

.. |Build Status| image:: https://img.shields.io/travis/zmqless/zeroless.svg?style=flat
   :target: https://travis-ci.org/zmqless/zeroless
.. |Coverage Status| image:: https://img.shields.io/coveralls/zmqless/zeroless.svg?style=flat
   :target: https://coveralls.io/r/zmqless/zeroless?branch=master
.. |Docs| image:: https://readthedocs.org/projects/zeroless/badge/?version=latest
   :target: https://readthedocs.org/projects/zeroless/?badge=latest
.. |License| image:: https://img.shields.io/pypi/l/zeroless.svg?style=flat
   :target: https://www.gnu.org/licenses/lgpl-2.1.html
.. |Codacy| image:: https://img.shields.io/codacy/116ada408f3c45709197e0e5d2fe46ba.svg?style=flat
   :target: https://www.codacy.com/p/4364
.. |PyPi| image:: https://img.shields.io/pypi/v/zeroless.svg?style=flat
   :target: https://pypi.python.org/pypi/zeroless

.. _ØMQ: http://www.zeromq.org
.. _ØMQGuide: http://zguide.zeromq.org
.. _PyZMQ: https://www.github.com/zeromq/pyzmq
.. _GitHub: https://github.com/zmqless/zeroless 
.. _Tracker: https://github.com/zmqless/zeroless/issues
.. _PyPy: https://pypi.python.org/pypi/zeroless


