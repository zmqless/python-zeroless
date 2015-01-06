from zeroless import Client

# Connects the client to as many servers as desired
client = Client()
client.connect_local(port=12345)

# Initiate a push client
# And assigns a callable to push messages
push = client.push()

for id, msg in [(b"1", b"Msg1"), (b"2", b"Msg2"), (b"3", b"Msg3")]:
    push(id, msg)
