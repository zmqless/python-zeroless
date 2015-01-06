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
