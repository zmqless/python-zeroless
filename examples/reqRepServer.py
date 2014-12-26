import logging

from zeroless import (bind, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The reply server binds to port 12345 and waits for incoming messages.
sock = bind(port=12345)

for msg in sock.listen_for_request():
    print(msg)
    sock.reply(msg)
