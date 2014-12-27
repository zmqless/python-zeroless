import pytest

from zeroless import (bind, connect)

@pytest.fixture(scope="module")
def sock1():
    return bind(port=7891)

@pytest.fixture(scope="module")
def sock2():
    return connect(port=7891)

class TestPushPull:
    def test_distribute(self, sock1, sock2):
        msg = b'msg'

        sock2.push(msg)
        result = next(sock1.listen_for_push())
        assert result == msg

    def test_distribute_multipart(self, sock1, sock2):
        msg1 = b'msg1'
        msg2 = b'msg2'

        sock2.push(msg1, msg2)
        result = next(sock1.listen_for_push())
        assert result == [msg1, msg2]

    def test_multiple_distribute(self, sock1, sock2):
        msgs = [b'msg' + bytes(i) for i in range(10)]

        for msg in msgs:
            sock2.push(msg)
            result = next(sock1.listen_for_push())
            assert result == msg

    def test_multiple_distribute_multipart(self, sock1, sock2):
        msgs1 = [b'msg1' + bytes(i) for i in range(10)]
        msgs2 = [b'msg2' + bytes(i) for i in range(10)]

        for msg1, msg2 in zip(msgs1, msgs2):
            sock2.push(msg1, msg2)
            result = next(sock1.listen_for_push())
            assert result == [msg1, msg2]
