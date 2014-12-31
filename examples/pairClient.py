import logging

from zeroless import (connect, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The pair client connects to localhost and sends three messages.
pair, listen_for_pair = connect(port=12345).pair()

for msg in [b"Msg1", b"Msg2", b"Msg3"]:
    pair(msg)
    response = next(listen_for_pair)
    print(response)
