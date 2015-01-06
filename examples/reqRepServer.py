import logging

from zeroless import (Server, log)

# Setup console logging
consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# Binds the reply server to port 12345
# And assigns a callable and an iterable
# To both transmit and wait for incoming messages
reply, listen_for_request = Server(port=12345).reply()

for msg in listen_for_request:
    print(msg)
    reply(msg)
