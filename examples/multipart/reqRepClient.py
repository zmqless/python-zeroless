from zeroless import connect

# The request client connects to localhost and sends three messages.
request, listen_for_reply = connect(port=12345).request()

for id, msg in [(b"1", b"Msg1"), (b"2", b"Msg2"), (b"3", b"Msg3")]:
    request(id, msg)
    response = next(listen_for_reply)
    print(response)
