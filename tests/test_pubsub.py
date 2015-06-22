import pytest

from time import sleep

from zeroless import (Server, Client)

@pytest.fixture(scope="module")
def listen_for_pub():
    client = Client()
    client.connect_local(port=7893)
    return client.sub()

@pytest.fixture(scope="module")
def pub():
    return Server(port=7893).pub()

@pytest.fixture(scope="module")
def listen_for_pub_with_topic():
    client = Client()
    client.connect_local(port=7895)
    return client.sub(topics=[b'sh'])

@pytest.fixture(scope="module")
def pub_with_topic():
    return Server(port=7895).pub(topic=b'sh')

@pytest.fixture(scope="module")
def listen_for_pub_with_embedded_topic():
    client = Client()
    client.connect_local(port=7894)
    return client.sub(topics=[b'sh'])

@pytest.fixture(scope="module")
def pub_with_embedded_topic():
    return Server(port=7894).pub(topic=b'sh', embed_topic=True)

@pytest.fixture(scope="module")
def listen_for_pub_with_empty_topic():
    client = Client()
    client.connect_local(port=7896)
    return client.sub()

@pytest.fixture(scope="module")
def pub_with_empty_topic():
    return Server(port=7896).pub(embed_topic=True)

class TestPubSub:
    def test_publish(self, pub, listen_for_pub):
        msg = b'msg'

        sleep(0.1)
        pub(msg)
        result = next(listen_for_pub)
        assert result == msg

    def test_publish_with_topic(self,
                                pub_with_topic,
                                listen_for_pub_with_topic):
        msg = b'sh msg'

        sleep(0.1)
        pub_with_topic(msg)
        result = next(listen_for_pub_with_topic)
        assert result == msg

    def test_publish_with_embedded_topic(self,
                                         pub_with_embedded_topic,
                                         listen_for_pub_with_embedded_topic):
        msg = b'msg'

        sleep(0.1)
        pub_with_embedded_topic(msg)
        result = next(listen_for_pub_with_embedded_topic)
        assert result == [b'sh', msg]

    def test_publish_with_empty_topic(self,
                                      pub_with_empty_topic,
                                      listen_for_pub_with_empty_topic):
        msg = b'msg'

        sleep(0.1)
        pub_with_empty_topic(msg)
        result = next(listen_for_pub_with_empty_topic)
        assert result == [b'', msg]

    def test_publish_multipart(self, pub, listen_for_pub):
        msg1 = b'msg1'
        msg2 = b'msg2'

        sleep(0.1)
        pub(msg1, msg2)
        result = next(listen_for_pub)
        assert result == [msg1, msg2]

    def test_multiple_publish(self, pub, listen_for_pub):
        msgs = [b'msg' + bytes(i) for i in range(10)]

        sleep(0.1)
        for msg in msgs:
            pub(msg)
            result = next(listen_for_pub)
            assert result == msg

    def test_multiple_publish_multipart(self, pub, listen_for_pub):
        msgs1 = [b'msg1' + bytes(i) for i in range(10)]
        msgs2 = [b'msg2' + bytes(i) for i in range(10)]

        sleep(0.1)
        for msg1, msg2 in zip(msgs1, msgs2):
            pub(msg1, msg2)
            result = next(listen_for_pub)
            assert result == [msg1, msg2]
