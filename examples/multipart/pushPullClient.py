from zeroless import connect

# The push client connects to localhost and sends three messages.
sock = connect(port=12345)

for id, msg in [(b"1", b"Msg1"), (b"2", b"Msg2"), (b"3", b"Msg3")]:
    sock.push(id, msg)
