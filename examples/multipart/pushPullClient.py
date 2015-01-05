from zeroless import Client

client = Client()
client.connect_local(port=12345)

# The push client connects to localhost and sends three messages.
push = client.push()

for id, msg in [(b"1", b"Msg1"), (b"2", b"Msg2"), (b"3", b"Msg3")]:
    push(id, msg)
