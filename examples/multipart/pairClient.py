from zeroless import Client

# Connects the client to a single server
client = Client()
client.connect_local(port=12345)

# Initiate a pair client
# And assigns a callable to transmit messages
pair, _ = client.pair()

for id, msg in [(b"1", b"Msg1"), (b"2", b"Msg2"), (b"3", b"Msg3")]:
    pair(id, msg)
