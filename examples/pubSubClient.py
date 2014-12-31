import logging

from time import sleep

from zeroless import (connect, log)

consoleHandler = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

# The publisher client connects to localhost and sends three messages.
pub = connect(port=12345).pub(topic=b'sh')

# Gives publisher some time to get initial subscriptions
sleep(1)

for msg in [b"Msg1", b"Msg2", b"Msg3"]:
    pub(msg)
