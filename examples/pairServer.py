import logging

from zeroless import (Server, log)

# Setup console logging
consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# Binds the pair server to port 12345
# And assigns a callable and an iterable
# To both transmit and wait for incoming messages
pair, listen_for_pair = Server(port=12345).pair()

for msg in listen_for_pair:
    print(msg)
    pair(msg)
