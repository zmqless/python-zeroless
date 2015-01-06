from zeroless import Server

from time import sleep

# Binds the publisher server to port 12345
# And assigns a callable to publish messages with no topic specified
pub = Server(port=12345).pub()

# Gives publisher some time to get initial subscriptions
sleep(1)

for id, msg in [(b"1", b"Msg1"), (b"2", b"Msg2"), (b"3", b"Msg3")]:
    pub(id, msg)
