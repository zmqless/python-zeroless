from zeroless import connect

# The pair client connects to localhost and sends three messages.
pair, _ = connect(port=12345).pair()

for id, msg in [(b"1", b"Msg1"), (b"2", b"Msg2"), (b"3", b"Msg3")]:
    pair(id, msg)
