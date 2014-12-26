import logging

from zeroless import (connect, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The pair client connects to localhost and sends three messages.
sock = connect(port=12345)

for msg in ["Msg1", "Msg2", "Msg3"]:
    sock.pair(msg.encode())
