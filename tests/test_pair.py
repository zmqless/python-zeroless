import pytest

from zeroless import (Server, Client)

@pytest.fixture(scope="module")
def listen_for_pair():
    _, listen = Server(port=7890).pair()
    return listen

@pytest.fixture(scope="module")
def pair():
    client = Client()
    client.connect_local(port=7890)
    send, _ = client.pair()
    return send

class TestPair:
    def test_ping_pong(self, pair, listen_for_pair):
        ping = b'ping'
        pong = b'pong'

        pair(ping)
        result = next(listen_for_pair)
        assert result == ping

        pair(pong)
        result = next(listen_for_pair)
        assert result == pong

    def test_ping_pong_multipart(self, pair, listen_for_pair):
        ping1 = b'ping1'
        ping2 = b'ping2'
        pong1 = b'pong1'
        pong2 = b'pong2'

        pair(ping1, ping2)
        result = next(listen_for_pair)
        assert result == [ping1, ping2]

        pair(pong1, pong2)
        result = next(listen_for_pair)
        assert result == [pong1, pong2]

    def test_multiple_ping_pong(self, pair, listen_for_pair):
        pings = [b'ping' + bytes(i) for i in range(10)]
        pongs = [b'pong' + bytes(i) for i in range(10)]

        for ping, pong in zip(pings, pongs):
            pair(ping)
            result = next(listen_for_pair)
            assert result == ping

            pair(pong)
            result = next(listen_for_pair)
            assert result == pong

    def test_multiple_ping_pong_multipart(self, pair, listen_for_pair):
        pings1 = [b'ping1' + bytes(i) for i in range(10)]
        pings2 = [b'ping2' + bytes(i) for i in range(10)]
        pongs1 = [b'pong1' + bytes(i) for i in range(10)]
        pongs2 = [b'pong2' + bytes(i) for i in range(10)]

        for ping1, ping2, pong1, pong2 in zip(pings1, pings2, pongs1, pongs2):
            pair(ping1, ping2)
            result = next(listen_for_pair)
            assert result == [ping1, ping2]

            pair(pong1, pong2)
            result = next(listen_for_pair)
            assert result == [pong1, pong2]
