import pytest

from zeroless import (Server, Client)

@pytest.fixture(scope="module")
def listen_for_push():
    return Server(port=7891).pull()

@pytest.fixture(scope="module")
def push():
    client = Client()
    client.connect_local(port=7891)
    return client.push()

class TestPushPull:
    def test_distribute(self, push, listen_for_push):
        msg = b'msg'

        push(msg)
        result = next(listen_for_push)
        assert result == msg

    def test_distribute_multipart(self, push, listen_for_push):
        msg1 = b'msg1'
        msg2 = b'msg2'

        push(msg1, msg2)
        result = next(listen_for_push)
        assert result == [msg1, msg2]

    def test_multiple_distribute(self, push, listen_for_push):
        msgs = [b'msg' + bytes(i) for i in range(10)]

        for msg in msgs:
            push(msg)
            result = next(listen_for_push)
            assert result == msg

    def test_multiple_distribute_multipart(self, push, listen_for_push):
        msgs1 = [b'msg1' + bytes(i) for i in range(10)]
        msgs2 = [b'msg2' + bytes(i) for i in range(10)]

        for msg1, msg2 in zip(msgs1, msgs2):
            push(msg1, msg2)
            result = next(listen_for_push)
            assert result == [msg1, msg2]
