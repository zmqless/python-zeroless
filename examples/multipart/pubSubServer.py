from zeroless import bind

# The subscriber server binds to port 12345 and waits for incoming messages.
listen_for_pub = bind(port=12345).sub()

for id, msg in listen_for_pub:
    print(id, ' - ', msg)
