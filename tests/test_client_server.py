import pytest

from zeroless import (Server, Client)

class TestClientServer:
    def test_server_port_property(self):
        port = 1050
        server = Server(port=port)

        assert server.port == port

    def test_client_addresses_property(self):
        client = Client()
        addresses = (('10.0.0.1', 1567), ('10.0.0.2', 1568), ('10.0.0.3', 1569))

        for ip, port in addresses:
            client.connect(ip, port)

        assert client.addresses == addresses