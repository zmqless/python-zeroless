import logging

from zeroless import (Server, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The reply server binds to port 12345 and waits for incoming messages.
reply, listen_for_request = Server(port=12345).reply()

for msg in listen_for_request:
    print(msg)
    reply(msg)
