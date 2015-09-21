import pytest

from zeroless import (Server, Client)

class TestExceptions:
    def test_port_under_range(self):
        client = Client()
        with pytest.raises(ValueError):
           client.connect_local(port=1023)

        with pytest.raises(ValueError):
           client.disconnect_local(port=1023)

        with pytest.raises(ValueError):
            Server(port=1023)

    def test_port_on_range(self):
        client = Client()
        client.connect_local(port=1024)
        client.disconnect_local(port=1024)
        client.connect_local(port=7000)
        client.disconnect_local(port=7000)
        client.connect_local(port=65535)
        client.disconnect_local(port=65535)

    def test_port_on_range_cascaded(self):
        Client()\
        .connect_local(port=1024)\
        .disconnect_local(port=1024)\
        .connect_local(port=7000)\
        .disconnect_local(port=7000)\
        .connect_local(port=65535)\
        .disconnect_local(port=65535)

    def test_port_after_range(self):
        client = Client()
        with pytest.raises(ValueError):
            client.connect_local(port=65536)

        with pytest.raises(ValueError):
            client.disconnect_local(port=65536)

        with pytest.raises(ValueError):
            Server(port=65536)

    def test_connection_after_pattern_was_established(self):
        client = Client()
        listen_for_push = client.pull()

        client.connect_local(port=1024)

        with pytest.raises(ValueError):
            client.connect_local(port=1024)

        client.disconnect_local(port=1024)

        with pytest.raises(ValueError):
            client.disconnect_local(port=1024)

    def test_there_was_no_connection_to_disconnect(self):
        client = Client()
        client.connect_local(port=1024)

        with pytest.raises(ValueError):
            client.disconnect_local(port=1025)

        client.disconnect_local(port=1024)

        with pytest.raises(ValueError):
            client.disconnect_local(port=1024)

    def test_connection_already_exist(self):
        client = Client()
        client.connect_local(port=1024)

        with pytest.raises(ValueError):
            client.connect_local(port=1024)

        client.disconnect_local(port=1024)
        client.connect_local(port=1024)

    def test_disconnect_all(self):
        client = Client()
        client.connect_local(port=1024)
        client.connect_local(port=1025)
        client.connect_local(port=1026)
        client.connect_local(port=1027)

        client.disconnect_all()

        client.connect_local(port=1024)
        client.connect_local(port=1025)
        client.connect_local(port=1026)
        client.connect_local(port=1027)

    def test_disconnect_all_cascaded(self):
        Client()\
        .connect_local(port=1024)\
        .connect_local(port=1025)\
        .connect_local(port=1026)\
        .connect_local(port=1027)\
        .disconnect_all()\
        .connect_local(port=1024)\
        .connect_local(port=1025)\
        .connect_local(port=1026)\
        .connect_local(port=1027)

    def test_port_already_used(self):
        listen_for_push = Server(port=65000).pull()

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

    def test_published_topic_is_not_included_into_message(self):
        pub = Server(port=7150).pub(topic=b'topic1')

        pub(b'topic1 msg')

        with pytest.raises(ValueError):
            pub(b'msg')

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
