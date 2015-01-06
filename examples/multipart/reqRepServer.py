from zeroless import Server

# Binds the reply server to port 12345
# And assigns a callable and an iterable
# To both transmit and wait for incoming messages
reply, listen_for_request = Server(port=12345).reply()

for id, msg in listen_for_request:
    print(id, ' - ', msg)
    reply(msg)
