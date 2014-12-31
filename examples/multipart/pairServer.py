from zeroless import bind

# The pair server binds to port 12345 and waits for incoming messages.
pair, listen_for_pair = bind(port=12345).pair()

for id, msg in listen_for_pair:
    print(id, ' - ', msg)
    pair(msg)
