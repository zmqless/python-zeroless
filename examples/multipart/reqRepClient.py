from zeroless import Client

# Connects the client to as many servers as desired
client = Client()
client.connect_local(port=12345)

# Initiate a request client
# And assigns a callable and an iterable
# To both transmit and wait for incoming messages
request, listen_for_reply = client.request()

for id, msg in [(b"1", b"Msg1"), (b"2", b"Msg2"), (b"3", b"Msg3")]:
    request(id, msg)
    response = next(listen_for_reply)
    print(response)
