from zeroless import bind

# The reply server binds to port 12345 and waits for incoming messages.
reply, listen_for_request = bind(port=12345).reply()

for id, msg in listen_for_request:
    print(id, ' - ', msg)
    reply(msg)
