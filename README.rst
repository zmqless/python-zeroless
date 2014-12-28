Zeroless
========

|Build Status| |Coverage Status|

Yet another `ZeroMQ <http://zeromq.org/>`__ wrapper for Python. However,
differing from `pyzmq <https://github.com/zeromq/pyzmq>`__, which tries
to stay very close to the C++ implementation, this project aims to make
distributed systems employing 0MQ as pythonic as possible.

Being simpler to use, Zeroless doesn't supports all of the fine aspects
and features of 0MQ. However, you can expect to find all the message
passing patterns you were accustomed to (i.e. pair, request/reply,
publisher/subscriber, push/pull). Depite that, the only transport
available is TCP, as threads are not as efficient in Python due to the
GIL and IPC is unix-only.

Installation
------------

.. code-block:: bash

    $ pip install zeroless

Python API
----------

In the ``zeroless`` module, two functions can be used to the define how
zeroless' sockets are related (i.e. ``bind`` and ``connect``). Both are
able to create a sort of generic 0MQ socket, which can then later become
an instance of a specific message passing pattern.

The generic socket object is both *callable* and *iterable*. So that you
can iterate over incoming messages, using the methods starting with
listen\_for\_\*, and/or call to transmit a message.

All examples assume:

.. code:: python

    from zeroless import (connect, bind)

Push-Pull
~~~~~~~~~

Useful for distributing the workload among a set of workers. A common
pattern in the Stream Processing field, being the cornestone of
applications like Apache Storm for instance. Also, it can be seen as a
generalisation of the Map-Reduce pattern.

.. code:: python

    # The pull server binds to port 12345 and waits for incoming messages.
    sock = bind(port=12345)

    for msg in sock.listen_for_pull():
        print(msg)

.. code:: python

    # The push client connects to localhost and sends three messages.
    sock = connect(port=12345)

    for msg in ["Msg1", "Msg2", "Msg3"]:
        sock.push(msg.encode())

Publisher-Subscriber
~~~~~~~~~~~~~~~~~~~~

Useful for broadcasting messages to a set of peers. A common pattern for
allowing real-time notifications at the client side, without having to
resort to inneficient approaches like pooling. Online services like
PubNub or IoT protocols like MQTT are examples of this pattern usage.

.. code:: python

    # The subscriber server binds to port 12345 and waits for incoming messages.
    sock = bind(port=12345)

    for msg in sock.listen_for_pub():
        print(msg)

.. code:: python

    # The publisher client connects to localhost and sends three messages.
    sock = connect(port=12345)

    for msg in ["Msg1", "Msg2", "Msg3"]:
        sock.pub(msg.encode())

Note: There is no support for topic usage, as ZMQ's topic filtering
capabilities are client side only.

Request-Reply
~~~~~~~~~~~~~

Useful for RPC style calls. A common pattern for clients to request data
and receive a response associated with the request. The HTTP protocol is
well-known for adopting this pattern, being it essential for Restful
services.

.. code:: python

    # The reply server binds to port 12345 and waits for incoming messages.
    sock = bind(port=12345)

    for msg in sock.listen_for_request():
        print(msg)
        sock.reply(msg)

.. code:: python

    # The request client connects to localhost and sends three messages.
    sock = connect(port=12345)

    for msg in ["Msg1", "Msg2", "Msg3"]:
        response = sock.request_and_listen(msg.encode())
        print(response)

Pair
~~~~

More often than not, this pattern will be unnecessary, as the above ones
or the mix of them suffices most use cases in distributed computing.
Regarding its capabilities, this pattern is the most similar alternative
to usual posix sockets among the aforementioned patterns. Therefore,
expect one-to-one and bidirectional communication.

.. code:: python

    # The pair server binds to port 12345 and waits for incoming messages.
    sock = bind(port=12345)

    for msg in sock.listen_for_pair():
        print(msg)
        sock.pair(msg)

.. code:: python

    # The pair client connects to localhost and sends three messages.
    sock = connect(port=12345)

    for msg in ["Msg1", "Msg2", "Msg3"]:
        sock.pair(msg.encode())

Logging
-------

The ``zeroless`` module allows logging via a global `Logger object <https://docs.python.org/3/library/logging.html#logger-objects>`__.

.. code:: python

    from zeroless import log

To enable it, just add an `Handler object <https://docs.python.org/3/library/logging.html#handler-objects>`__ and set an appropriate `logging level <https://docs.python.org/3/library/logging.html#logging-levels>`__.

Testing
-------

To run individual tests:

.. code-block:: bash

    $ py.test tests/test_desired_module.py

To run all the tests:

.. code-block:: bash

    $ python setup.py test

Alternatively, you can use tox:

.. code-block:: bash

    $ tox

License
-------

Copyright 2014 Lucas Lira Gomes x8lucas8x@gmail.com

This library is free software; you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or (at
your option) any later version.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library. If not, see http://www.gnu.org/licenses/.

.. |Build Status| image:: https://travis-ci.org/zmqless/zeroless.svg?branch=master
   :target: https://travis-ci.org/zmqless/zeroless
.. |Coverage Status| image:: https://coveralls.io/repos/zmqless/zeroless/badge.png?branch=master
   :target: https://coveralls.io/r/zmqless/zeroless?branch=master
