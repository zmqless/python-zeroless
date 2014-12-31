import logging

from zeroless import (bind, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The pull server binds to port 12345 and waits for incoming messages.
listen_for_push = bind(port=12345).pull()

for msg in listen_for_push:
    print(msg)
