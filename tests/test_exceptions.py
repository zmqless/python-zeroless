import pytest

from zeroless import(Server, Client)

class TestExceptions:
    def test_port_under_range(self):
        client = Client()
        with pytest.raises(ValueError):
           client.connect_local(port=1023)

        with pytest.raises(ValueError):
            Server(port=1023)

    def test_port_on_range(self):
        client = Client()
        client.connect_local(port=1024)
        client.connect_local(port=7000)
        client.connect_local(port=65535)

    def test_port_after_range(self):
        client = Client()
        with pytest.raises(ValueError):
            client.connect_local(port=65536)

        with pytest.raises(ValueError):
            Server(port=65536)

    def test_port_already_used(self):
        server1 = Server(port=65000).pull()

        with pytest.raises(ValueError):
            Server(port=65000).pull()

    def test_data_is_not_bytes(self):
        client = Client()
        client.connect_local(port=7050)
        push = client.push()

        with pytest.raises(TypeError):
            push(u'msg')

    def test_published_topic_is_not_bytes(self):
        Server(port=7099).pub(topic=b'topic1')

        with pytest.raises(TypeError):
            Server(port=7100).pub(topic=u'topic1')

    def test_subscribed_topics_are_not_bytes(self):
        client = Client()
        client.connect_local(port=7099)

        client.sub(topics=[b'topic1'])

        with pytest.raises(TypeError):
            client.sub(topics=[u'topic1'])

        with pytest.raises(TypeError):
            client.sub(topics=[b'topic1', u'topic2'])

    def test_pair_client_cannot_connect_more_than_once(self):
        client = Client()
        client.connect_local(port=7200)
        client.connect_local(port=7201)

        with pytest.raises(RuntimeError):
            client.pair()

        client = Client()
        client.connect_local(port=7200)

        client.pair()

        with pytest.raises(RuntimeError):
            client.connect_local(port=7201)

