from zeroless import connect

# The subscriber server binds to port 12345 and waits for incoming messages.
listen_for_pub = connect(port=12345).sub()

for topic, id, msg in listen_for_pub:
    print(topic, ' - ', id, ' - ', msg)
