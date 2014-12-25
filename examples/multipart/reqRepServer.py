from zeroless import bind

# The reply server binds to port 12345 and waits for incoming messages.
sock = bind(port=12345)

for id, msg in sock.listen_for_request():
    print(id, ' - ', msg)
    sock.reply(msg)
