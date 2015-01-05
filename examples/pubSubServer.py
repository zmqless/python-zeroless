import logging

from zeroless import (Client, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

client = Client()
client.connect_local(port=12345)

# The subscriber server binds to port 12345 and waits for incoming messages.
listen_for_pub = client.sub(topics=[b'sh'])

for topic, msg in listen_for_pub:
    print(topic, ' - ', msg)
