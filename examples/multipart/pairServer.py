from zeroless import bind

# The pair server binds to port 12345 and waits for incoming messages.
sock = bind(port=12345)

for id, msg in sock.listen_for_pair():
    print(id, ' - ', msg)
    sock.pair(msg)
