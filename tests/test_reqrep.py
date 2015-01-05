import pytest

from zeroless import (Server, Client)

@pytest.fixture(scope="module")
def reply_gens():
    return Server(port=7892).reply()

@pytest.fixture(scope="module")
def request_gens():
    client = Client()
    client.connect_local(port=7892)
    return client.request()

class TestReqRep:
    def test_ping_pong(self, request_gens, reply_gens):
        request, listen_for_reply = request_gens
        reply, listen_for_request = reply_gens

        ping = b'ping'
        pong = b'pong'

        request(ping)
        result = next(listen_for_request)
        assert result == ping

        reply(pong)
        result = next(listen_for_reply)
        assert result == pong

    def test_ping_pong_multipart(self, request_gens, reply_gens):
        request, listen_for_reply = request_gens
        reply, listen_for_request = reply_gens

        ping1 = b'ping1'
        ping2 = b'ping2'
        pong1 = b'pong1'
        pong2 = b'pong2'

        request(ping1, ping2)
        result = next(listen_for_request)
        assert result == [ping1, ping2]

        reply(pong1, pong2)
        result = next(listen_for_reply)
        assert result == [pong1, pong2]

    def test_multiple_ping_pong(self, request_gens, reply_gens):
        request, listen_for_reply = request_gens
        reply, listen_for_request = reply_gens

        pings = [b'ping' + bytes(i) for i in range(10)]
        pongs = [b'pong' + bytes(i) for i in range(10)]

        for ping, pong in zip(pings, pongs):
            request(ping)
            result = next(listen_for_request)
            assert result == ping

            reply(pong)
            result = next(listen_for_reply)
            assert result == pong

    def test_multiple_ping_pong_multipart(self, request_gens, reply_gens):
        request, listen_for_reply = request_gens
        reply, listen_for_request = reply_gens

        pings1 = [b'ping1' + bytes(i) for i in range(10)]
        pings2 = [b'ping2' + bytes(i) for i in range(10)]
        pongs1 = [b'pong1' + bytes(i) for i in range(10)]
        pongs2 = [b'pong2' + bytes(i) for i in range(10)]

        for ping1, ping2, pong1, pong2 in zip(pings1, pings2, pongs1, pongs2):
            request(ping1, ping2)
            result = next(listen_for_request)
            assert result == [ping1, ping2]

            reply(pong1, pong2)
            result = next(listen_for_reply)
            assert result == [pong1, pong2]
