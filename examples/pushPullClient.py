import logging

from zeroless import (Client, log)

# Setup console logging
consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# Connects the client to as many servers as desired
client = Client()
client.connect_local(port=12345)

# Initiate a push client
# And assigns a callable to push messages
push = client.push()

for msg in [b"Msg1", b"Msg2", b"Msg3"]:
    push(msg)
