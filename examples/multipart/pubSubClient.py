from zeroless import connect

from time import sleep

# The publisher client connects to localhost and sends three messages.
pub = connect(port=12345).pub()

# Gives publisher some time to get initial subscriptions
sleep(1)

for id, msg in [(b"1", b"Msg1"), (b"2", b"Msg2"), (b"3", b"Msg3")]:
    pub(id, msg)
