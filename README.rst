Zeroless
========

.. _badges_start:

|Build Status| |Coverage Status| |Codacy| |PyPi| |Docs| |License|

.. _badges_end:

Yet another ØMQ_ wrapper for Python. However, differing from PyZMQ_, which
tries to stay very close to the C++ implementation, this project aims to
make distributed systems employing ØMQ_ as pythonic as possible.

Being simpler to use, Zeroless doesn't supports all of the fine aspects
and features of ØMQ_. However, you can expect to find all the message
passing patterns you were accustomed to (i.e. pair, request/reply,
publisher/subscriber, push/pull). Depite that, the only transport
available is TCP, as threads are not as efficient in Python due to the
GIL and IPC is unix-only.

Installation
------------

.. _install_content_start:

.. code-block:: bash

    $ pip install zeroless

.. _install_content_end:

Python API
----------

.. _python_api_content_start:

In the ``zeroless`` module, two classes can be used to define how distributed
entities are related (i.e. ``Server`` and ``Client``). To put it bluntly, with
the exception of the pair pattern, a client may be connected to multiple
servers, while a server may accept incoming connections from multiple clients.

Both servers and clients are able to create a *callable* and/or *iterable*,
depending on the message passing pattern. So that you can iterate over incoming
messages and/or call to transmit a message.

.. _python_api_content_end:

All examples assume:

.. code:: python

    from zeroless import (Server, Client)

Push-Pull
~~~~~~~~~

.. _push_pull_content_start:

Useful for distributing the workload among a set of workers. A common
pattern in the Stream Processing field, being the cornestone of
applications like Apache Storm for instance. Also, it can be seen as a
generalisation of the Map-Reduce pattern.

.. _push_pull_content_end:

.. code:: python

    # Binds the pull server to port 12345
    # And assigns an iterable to wait for incoming messages
    listen_for_push = Server(port=12345).pull()

    for msg in listen_for_push:
        print(msg)

.. code:: python

    # Connects the client to as many servers as desired
    client = Client()
    client.connect_local(port=12345)

    # Initiate a push client
    # And assigns a callable to push messages
    push = client.push()

    for msg in [b"Msg1", b"Msg2", b"Msg3"]:
        push(msg)

Publisher-Subscriber
~~~~~~~~~~~~~~~~~~~~

.. _pub_sub_content_start:

Useful for broadcasting messages to a set of peers. A common pattern for
allowing real-time notifications at the client side, without having to
resort to inneficient approaches like pooling. Online services like
PubNub or IoT protocols like MQTT are examples of this pattern usage.

.. _pub_sub_content_end:

.. code:: python

    # Binds the publisher server to port 12345
    # And assigns a callable to publish messages with the topic 'sh'
    pub = Server(port=12345).pub(topic=b'sh', embed_topic=True)

    # Gives publisher some time to get initial subscriptions
    sleep(1)

    for msg in [b"Msg1", b"Msg2", b"Msg3"]:
        pub(msg)

.. code:: python

    # Connects the client to as many servers as desired
    client = Client()
    client.connect_local(port=12345)

    # Initiate a subscriber client
    # Assigns an iterable to wait for incoming messages with the topic 'sh'
    listen_for_pub = client.sub(topics=[b'sh'])

    for topic, msg in listen_for_pub:
        print(topic, ' - ', msg)

.. _pub_sub_appendix_start:

Note: ZMQ's topic filtering capabilities are publisher side since ZMQ 3.0.

Last but not least, SUB sockets that bind will not get any message before they
first ask for via the provided generator, so prefer to bind PUB sockets if
missing some messages is not an option.

.. _pub_sub_appendix_end:

Request-Reply
~~~~~~~~~~~~~

.. _req_rep_content_start:

Useful for RPC style calls. A common pattern for clients to request data
and receive a response associated with the request. The HTTP protocol is
well-known for adopting this pattern, being it essential for Restful
services.

.. _req_rep_content_end:

.. code:: python

    # Binds the reply server to port 12345
    # And assigns a callable and an iterable
    # To both transmit and wait for incoming messages
    reply, listen_for_request = Server(port=12345).reply()

    for msg in listen_for_request:
        print(msg)
        reply(msg)

.. code:: python

    # Connects the client to as many servers as desired
    client = Client()
    client.connect_local(port=12345)

    # Initiate a request client
    # And assigns a callable and an iterable
    # To both transmit and wait for incoming messages
    request, listen_for_reply = client.request()

    for msg in [b"Msg1", b"Msg2", b"Msg3"]:
        request(msg)
        response = next(listen_for_reply)
        print(response)

Pair
~~~~

.. _pair_content_start:

More often than not, this pattern will be unnecessary, as the above ones
or the mix of them suffices most use cases in distributed computing.
Regarding its capabilities, this pattern is the most similar alternative
to usual posix sockets among the aforementioned patterns. Therefore,
expect one-to-one and bidirectional communication.

.. _pair_content_end:

.. code:: python

    # Binds the pair server to port 12345
    # And assigns a callable and an iterable
    # To both transmit and wait for incoming messages
    pair, listen_for_pair = Server(port=12345).pair()

    for msg in listen_for_pair:
        print(msg)
        pair(msg)

.. code:: python

    # Connects the client to a single server
    client = Client()
    client.connect_local(port=12345)

    # Initiate a pair client
    # And assigns a callable and an iterable
    # To both transmit and wait for incoming messages
    pair, listen_for_pair = client.pair()

    for msg in [b"Msg1", b"Msg2", b"Msg3"]:
        pair(msg)
        response = next(listen_for_pair)
        print(response)

Logging
-------

.. _logging_content_start:

The ``zeroless`` module allows logging via a global `Logger object <https://docs.python.org/3/library/logging.html#logger-objects>`__.

.. code:: python

    from zeroless import log

To enable it, just add an `Handler object <https://docs.python.org/3/library/logging.html#handler-objects>`__ and set an appropriate `logging level <https://docs.python.org/3/library/logging.html#logging-levels>`__.

.. _logging_content_end:

Testing
-------

.. _testing_content_start:

To run individual tests:

.. code-block:: bash

    $ py.test tests/test_desired_module.py

To run all the tests:

.. code-block:: bash

    $ python setup.py test

Alternatively, you can use tox:

.. code-block:: bash

    $ tox

.. _testing_content_end:

Need help?
----------

For more information, please see our documentation_.

License
-------

.. _license_content_start:

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

.. _license_content_end:

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
.. _PyZMQ: https://www.github.com/zeromq/pyzmq
.. _documentation: http://zeroless.readthedocs.org/en/latest/
