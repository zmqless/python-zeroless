from zeroless import Server

# The pull server binds to port 12345 and waits for incoming messages.
listen_for_push = Server(port=12345).pull()

for id, msg in listen_for_push:
    print(id, ' - ', msg)
