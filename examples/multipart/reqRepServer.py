from zeroless import Server

# The reply server binds to port 12345 and waits for incoming messages.
reply, listen_for_request = Server(port=12345).reply()

for id, msg in listen_for_request:
    print(id, ' - ', msg)
    reply(msg)
