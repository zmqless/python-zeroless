import logging

from zeroless import (Client, log)

# Setup console logging
consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# Connects the client to as many servers as desired
client = Client()
client.connect_local(port=12345)

# Initiate a subscriber client
# Assigns an iterable to wait for incoming messages with the topic 'sh'
listen_for_pub = client.sub(topics=[b'sh'])

for topic, msg in listen_for_pub:
    print(topic, ' - ', msg)
