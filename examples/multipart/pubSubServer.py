from zeroless import Client

# Connects the client to as many servers as desired
client = Client()
client.connect_local(port=12345)

# Initiate a subscriber client
# Assigns an iterable to wait for incoming messages with any topic
listen_for_pub = client.sub()

for topic, id, msg in listen_for_pub:
    print(topic, ' - ', id, ' - ', msg)
