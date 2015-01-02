.. _quickstart:

Quickstart
----------

In the ``zeroless`` module, two functions can be used to define how
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

Last but not least, SUB sockets that bind will not get any message before they
first ask for via the provided generator, so prefer to bind PUB sockets if
missing some messages is not an option.

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
