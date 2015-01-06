import logging

from zeroless import (Client, log)

# Setup console logging
consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# Connects the client to a single server
client = Client()
client.connect_local(port=12345)

# Initiate a pair client
# And assigns a callable and an iterable
# To both transmit and wait for incoming messages
pair, listen_for_pair = client.pair()

for msg in [b"Msg1", b"Msg2", b"Msg3"]:
    pair(msg)
    response = next(listen_for_pair)
    print(response)
