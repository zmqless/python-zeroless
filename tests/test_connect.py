import pytest

from zeroless import(connect, ConnectSock)

@pytest.fixture(scope="module")
def sock2():
    return connect(port=7890)

class TestConnect:
    def test_connect(self, sock2):
        assert isinstance(sock2, ConnectSock)
