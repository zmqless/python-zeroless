import pytest

from zeroless import (Server)

class TestClientServer:
    def test_server_port_property(self):
        port = 1050
        server = Server(port=port)

        assert server.port == port