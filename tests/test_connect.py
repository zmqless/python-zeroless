import pytest

from zeroless import(connect, ConnectSock)

class TestConnect:
    def connect(self):
        assert isinstance(connect(port=12345), ConnectSock)
