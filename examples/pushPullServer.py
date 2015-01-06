import logging

from zeroless import (Server, log)

# Setup console logging
consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# Binds the pull server to port 12345
# And assigns an iterable to wait for incoming messages
listen_for_push = Server(port=12345).pull()

for msg in listen_for_push:
    print(msg)
