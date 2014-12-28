import pytest

from zeroless import(bind, BindSock)

@pytest.fixture(scope="module")
def sock1():
    return bind(port=7890)

class TestBind:
    def test_bind(self, sock1):
        assert isinstance(sock1, BindSock)
