import logging

from zeroless import (connect, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The subscriber server binds to port 12345 and waits for incoming messages.
listen_for_pub = connect(port=12345).sub(topics=[b'sh'])

for topic, msg in listen_for_pub:
    print(topic, ' - ', msg)
