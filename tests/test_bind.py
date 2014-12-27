import pytest

from zeroless import(bind, BindSock)

class TestBind:
    def connect(self):
        assert isinstance(bind(port=12345), BindSock)
