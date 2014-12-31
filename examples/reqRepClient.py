import logging

from zeroless import (connect, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The request client connects to localhost and sends three messages.
request, listen_for_reply = connect(port=12345).request()

for msg in [b"Msg1", b"Msg2", b"Msg3"]:
    request(msg)
    response = next(listen_for_reply)
    print(response)
