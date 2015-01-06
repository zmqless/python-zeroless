.. _quickstart:

Quickstart
----------

.. include:: ../README.rst
   :start-after: _python_api_content_start:
   :end-before:  _python_api_content_end:

Message Passing Patterns
------------------------

Zeroless supports the following message passing patterns:

Push-Pull
~~~~~~~~~

.. include:: ../README.rst
   :start-after: _push_pull_content_start:
   :end-before:  _push_pull_content_end:

.. literalinclude:: ../examples/pushPullServer.py
   :language: python 

.. literalinclude:: ../examples/pushPullClient.py
   :language: python 

Publisher-Subscriber
~~~~~~~~~~~~~~~~~~~~

.. include:: ../README.rst
   :start-after: _pub_sub_content_start:
   :end-before:  _pub_sub_content_end:

.. literalinclude:: ../examples/pubSubServer.py
   :language: python 

.. literalinclude:: ../examples/pubSubClient.py
   :language: python 

.. include:: ../README.rst
   :start-after: _pub_sub_appendix_start:
   :end-before:  _pub_sub_appendix_end:

Request-Reply
~~~~~~~~~~~~~

.. include:: ../README.rst
   :start-after: _req_rep_content_start:
   :end-before:  _req_rep_content_end:

.. literalinclude:: ../examples/reqRepServer.py
   :language: python 

.. literalinclude:: ../examples/reqRepClient.py
   :language: python 

Pair
~~~~

.. include:: ../README.rst
   :start-after: _pair_content_start:
   :end-before:  _pair_content_end:

.. literalinclude:: ../examples/pairServer.py
   :language: python 

.. literalinclude:: ../examples/pairClient.py
   :language: python 

Additional Features
-------------------

Logging
~~~~~~~

Python provides a wonderfull ``logging`` module. It can be used to track
Zeroless' internal workflow in a modular way, therefore being very useful
for debugging purposes.

.. include:: ../README.rst
   :start-after: _logging_content_start:
   :end-before:  _logging_content_end:

Multipart Messages
~~~~~~~~~~~~~~~~~~

In the Zeroless API, all *callables* have a ``print`` like signature, therefore
being able to have an infinite number of arguments. Each of these arguments are
part of the whole message, that could be divided in multiple pieces. Being that
useful when you have a simple message structure, with just a few fields, and
don't want to rely on a data formatting standard (e.g. JSoN, XML) to maintain
the message semantics. Also, given the need to parse those different parts that
a single message may have, the receiver's *iterable* will return them all, at
once, in transparent fashion.

For more on this, see the examples/multipart folder or check the following
example:

.. literalinclude:: ../examples/multipart/pushPullServer.py
   :language: python 

.. literalinclude:: ../examples/multipart/pushPullClient.py
   :language: python 
