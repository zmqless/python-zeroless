import logging

from zeroless import (Server, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The pair server binds to port 12345 and waits for incoming messages.
pair, listen_for_pair = Server(port=12345).pair()

for msg in listen_for_pair:
    print(msg)
    pair(msg)
