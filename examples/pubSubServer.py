from zeroless import bind

# The subscriber server binds to port 12345 and waits for incoming messages.
sock = bind(port=12345)

for msg in sock.listen_for_pub():
    print(msg)
