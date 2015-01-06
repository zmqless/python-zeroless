from zeroless import Server

# Binds the pair server to port 12345
# And assigns a callable and an iterable
# To both transmit and wait for incoming messages
pair, listen_for_pair = Server(port=12345).pair()

for id, msg in listen_for_pair:
    print(id, ' - ', msg)
    pair(msg)
