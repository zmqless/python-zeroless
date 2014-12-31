from zeroless import bind

# The pull server binds to port 12345 and waits for incoming messages.
listen_for_push = bind(port=12345).pull()

for id, msg in listen_for_push:
    print(id, ' - ', msg)
