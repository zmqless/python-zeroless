import logging

from zeroless import (Client, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

client = Client()
client.connect_local(port=12345)

# The request client connects to localhost and sends three messages.
request, listen_for_reply = client.request()

for msg in [b"Msg1", b"Msg2", b"Msg3"]:
    request(msg)
    response = next(listen_for_reply)
    print(response)
