import logging

from zeroless import (Client, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

client = Client()
client.connect_local(port=12345)

# The pair client connects to localhost and sends three messages.
pair, listen_for_pair = client.pair()

for msg in [b"Msg1", b"Msg2", b"Msg3"]:
    pair(msg)
    response = next(listen_for_pair)
    print(response)
