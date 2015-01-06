from zeroless import Server

# Binds the pull server to port 12345
# And assigns an iterable to wait for incoming messages
listen_for_push = Server(port=12345).pull()

for id, msg in listen_for_push:
    print(id, ' - ', msg)
