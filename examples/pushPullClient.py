import logging

from zeroless import (connect, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The push client connects to localhost and sends three messages.
push = connect(port=12345).push()

for msg in [b"Msg1", b"Msg2", b"Msg3"]:
    push(msg)
