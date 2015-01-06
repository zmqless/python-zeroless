import logging

from zeroless import (Client, log)

# Setup console logging
consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# Connects the client to as many servers as desired
client = Client()
client.connect_local(port=12345)

# Initiate a request client
# And assigns a callable and an iterable
# To both transmit and wait for incoming messages
request, listen_for_reply = client.request()

for msg in [b"Msg1", b"Msg2", b"Msg3"]:
    request(msg)
    response = next(listen_for_reply)
    print(response)
