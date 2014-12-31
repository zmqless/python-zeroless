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
able to create a *callable* and/or *iterable* socket, depending on the
message passing pattern.

So that you can iterate over incoming messages and/or call to transmit a
message.

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
    listen_for_push = bind(port=12345).pull()

    for msg in listen_for_push:
        print(msg)

.. code:: python

    # The push client connects to localhost and sends three messages.
    push = connect(port=12345).push()

    for msg in [b"Msg1", b"Msg2", b"Msg3"]:
        push(msg)

Publisher-Subscriber
~~~~~~~~~~~~~~~~~~~~

Useful for broadcasting messages to a set of peers. A common pattern for
allowing real-time notifications at the client side, without having to
resort to inneficient approaches like pooling. Online services like
PubNub or IoT protocols like MQTT are examples of this pattern usage.

.. code:: python

    # The publisher server connects to localhost and sends three messages.
    pub = bind(port=12345).pub(topic=b'sh')

    # Gives publisher some time to get initial subscriptions
    sleep(1)

    for msg in [b"Msg1", b"Msg2", b"Msg3"]:
        pub(msg)

.. code:: python

    # The subscriber client binds to port 12345 and waits for incoming messages.
    listen_for_pub = connect(port=12345).sub(topics=[b'sh'])

    for topic, msg in listen_for_pub:
        print(topic, ' - ', msg)

Note: ZMQ's topic filtering capabilities are publisher side since ZMQ 3.0.

Warning: SUB sockets that bind will not get any message before they first ask
         for via the provided generator, so prefer to bind PUB sockets if missing
         some messages is not an option.

Request-Reply
~~~~~~~~~~~~~

Useful for RPC style calls. A common pattern for clients to request data
and receive a response associated with the request. The HTTP protocol is
well-known for adopting this pattern, being it essential for Restful
services.

.. code:: python

    # The reply server binds to port 12345 and waits for incoming messages.
    reply, listen_for_request = bind(port=12345).reply()

    for msg in listen_for_request:
        print(msg)
        reply(msg)

.. code:: python

    # The request client connects to localhost and sends three messages.
    request, listen_for_reply = connect(port=12345).request()

    for msg in [b"Msg1", b"Msg2", b"Msg3"]:
        request(msg)
        response = next(listen_for_reply)
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
    pair, listen_for_pair = bind(port=12345).pair()

    for msg in listen_for_pair:
        print(msg)
        pair(msg)

.. code:: python

    # The pair client connects to localhost and sends three messages.
    pair, listen_for_pair = connect(port=12345).pair()

    for msg in [b"Msg1", b"Msg2", b"Msg3"]:
        pair(msg)
        response = next(listen_for_pair)
        print(response)

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
