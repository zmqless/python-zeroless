from zeroless import Client

client = Client()
client.connect_local(port=12345)

# The subscriber server binds to port 12345 and waits for incoming messages.
listen_for_pub = client.sub()

for topic, id, msg in listen_for_pub:
    print(topic, ' - ', id, ' - ', msg)
