import logging

from zeroless import (Client, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

client = Client()
client.connect_local(port=12345)

# The push client connects to localhost and sends three messages.
push = client.push()

for msg in [b"Msg1", b"Msg2", b"Msg3"]:
    push(msg)
