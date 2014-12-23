from zeroless import connect

# The push client connects to localhost and sends three messages.
sock = connect(port=12345)

for msg in ["Msg1", "Msg2", "Msg3"]:
    sock.push(msg.encode())
