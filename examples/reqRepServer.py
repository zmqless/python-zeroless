import logging

from zeroless import (bind, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The reply server binds to port 12345 and waits for incoming messages.
reply, listen_for_request = bind(port=12345).reply()

for msg in listen_for_request:
    print(msg)
    reply(msg)
