import pytest

from time import sleep

from zeroless import (bind, connect)

@pytest.fixture(scope="module")
def listen_for_pub():
    return connect(port=7893).sub()

@pytest.fixture(scope="module")
def pub():
    return bind(port=7893).pub()

@pytest.fixture(scope="module")
def listen_for_pub_with_topic():
    return connect(port=7894).sub(topics=[b'sh'])

@pytest.fixture(scope="module")
def pub_with_topic():
    return bind(port=7894).pub(topic=b'sh')

class TestPubSub:
    def test_publish(self, pub, listen_for_pub):
        msg = b'msg'

        pub(msg)
        result = next(listen_for_pub)
        assert result == [b'', msg]

    def test_publish_with_topic(self, pub_with_topic, listen_for_pub_with_topic):
        msg = b'msg'

        pub_with_topic(msg)
        result = next(listen_for_pub_with_topic)
        assert result != [b'', msg]
        assert result == [b'sh', msg]

    def test_publish_multipart(self, pub, listen_for_pub):
        msg1 = b'msg1'
        msg2 = b'msg2'

        pub(msg1, msg2)
        result = next(listen_for_pub)
        assert result == [b'', msg1, msg2]

    def test_multiple_publish(self, pub, listen_for_pub):
        msgs = [b'msg' + bytes(i) for i in range(10)]

        for msg in msgs:
            pub(msg)
            result = next(listen_for_pub)
            assert result == [b'', msg]

    def test_multiple_publish_multipart(self, pub, listen_for_pub):
        msgs1 = [b'msg1' + bytes(i) for i in range(10)]
        msgs2 = [b'msg2' + bytes(i) for i in range(10)]

        for msg1, msg2 in zip(msgs1, msgs2):
            pub(msg1, msg2)
            result = next(listen_for_pub)
            assert result == [b'', msg1, msg2]
