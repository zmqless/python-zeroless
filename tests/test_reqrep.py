import pytest

from zeroless import (bind, connect)

@pytest.fixture(scope="module")
def sock1():
    return bind(port=7892)

@pytest.fixture(scope="module")
def sock2():
    return connect(port=7892)

class TestReqRep:
    def test_ping_pong(self, sock1, sock2):
        ping = b'ping'
        pong = b'pong'

        sock2.request(ping)
        result = next(sock1.listen_for_request())
        assert result == ping

        sock1.reply(pong)
        result = next(sock2.listen_for_reply())
        assert result == pong

    def test_ping_pong_multipart(self, sock1, sock2):
        ping1 = b'ping1'
        ping2 = b'ping2'
        pong1 = b'pong1'
        pong2 = b'pong2'

        sock2.request(ping1, ping2)
        result = next(sock1.listen_for_request())
        assert result == [ping1, ping2]

        sock1.reply(pong1, pong2)
        result = next(sock2.listen_for_reply())
        assert result == [pong1, pong2]

    def test_multiple_ping_pong(self, sock1, sock2):
        pings = [b'ping' + bytes(i) for i in range(10)]
        pongs = [b'pong' + bytes(i) for i in range(10)]

        for ping, pong in zip(pings, pongs):
            sock2.request(ping)
            result = next(sock1.listen_for_request())
            assert result == ping

            sock1.reply(pong)
            result = next(sock2.listen_for_reply())
            assert result == pong

    def test_multiple_ping_pong_multipart(self, sock1, sock2):
        pings1 = [b'ping1' + bytes(i) for i in range(10)]
        pings2 = [b'ping2' + bytes(i) for i in range(10)]
        pongs1 = [b'pong1' + bytes(i) for i in range(10)]
        pongs2 = [b'pong2' + bytes(i) for i in range(10)]

        for ping1, ping2, pong1, pong2 in zip(pings1, pings2, pongs1, pongs2):
            sock2.request(ping1, ping2)
            result = next(sock1.listen_for_request())
            assert result == [ping1, ping2]

            sock1.reply(pong1, pong2)
            result = next(sock2.listen_for_reply())
            assert result == [pong1, pong2]
