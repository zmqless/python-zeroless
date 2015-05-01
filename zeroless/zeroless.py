"""
The Zeroless module API.

.. data:: log

A global Logger object. To use it, just add an Handler object
and set an appropriate logging level.
"""

import zmq
import logging

from time import sleep
from copy import deepcopy
from warnings import warn
from functools import partial

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

def _check_valid_port_range(port):
    if port < 1024 or port > 65535:
        error = 'Port {0} is invalid, choose one between 1024 and 65535'
        error = error.format(port)
        log.error(error)
        raise ValueError(error)

def _check_valid_num_connections(socket_type, num_connections):
    if socket_type == zmq.PAIR and num_connections > 1:
        error = 'A client cannot connect more than once in the PAIR pattern'
        log.error(error)
        raise RuntimeError(error)

def _connect_zmq_sock(sock, ip, port):
    log.info('Connecting to {0} on port {1}'.format(ip, port))
    sock.connect('tcp://' + ip + ':' + str(port))

def _disconnect_zmq_sock(sock, ip, port):
    log.info('Disconnecting from {0} on port {1}'.format(ip, port))

    try:
        sock.disconnect('tcp://' + ip + ':' + str(port))
    except zmq.ZMQError:
        error = 'There was no connection to {0} on port {1}'.format(ip, port)
        log.exception(error)
        raise ValueError(error)

def _bind_zmq_sock(sock, port):
    log.info('Binding on port {0}'.format(port))

    try:
        sock.bind('tcp://*:' + str(port))
    except zmq.ZMQError:
        error = 'Port {0} is already in use'.format(port)
        log.exception(error)
        raise ValueError(error)

def _recv(sock):
    while True:
        frames = sock.recv_multipart()
        log.debug('Receiving: {0}'.format(frames))
        yield frames if len(frames) > 1 else frames[0]

class Sock:
    def __init__(self):
        pass

    def __sock(self, pattern):
        sock = zmq.Context().instance().socket(pattern)
        self._setup(sock)

        log.info('Ready...')

        return sock

    def __send_function(self, sock, topic=None, embed_topic=False):
        def _send(*data):
            log.debug('Sending: {0}'.format(data))

            try:
                sock.send_multipart(data)
            except TypeError:
                error = 'Data must be bytes, so try again'
                log.exception(error)
                raise TypeError(error)

        if sock.socket_type == zmq.PUB and embed_topic:
            if topic:
                return partial(_send, topic)
            else:
                return partial(_send, b'')

        return _send

    def __recv_generator(self, sock):
        return _recv(sock)

    # PubSub pattern
    def pub(self, topic=b'', embed_topic=False):
        """
        Returns a callable that can be used to transmit a message, with a given
        ``topic``, in a publisher-subscriber fashion. Note that the sender
        function has a ``print`` like signature, with an infinite number of
        arguments. Each one being a part of the complete message.

        :param topic: the topic that will be published to (default=b'')
        :type topic: bytes
        :param embed_topic: set to embed the topic into published messages
                            (default=False)
        :type embed_topic bool
        :rtype: function
        """
        if not isinstance(topic, bytes):
            error = 'Topic must be bytes'
            log.error(error)
            raise TypeError(error)

        sock = self.__sock(zmq.PUB)
        return self.__send_function(sock, topic, embed_topic)

    def sub(self, topics=(b'',)):
        """
        Returns an iterable that can be used to iterate over incoming messages,
        that were published with one of the topics specified in ``topics``. Note
        that the iterable returns as many parts as sent by subscribed publishers.

        :param topics: a list of topics to subscribe to (default=b'')
        :type topics: list of bytes
        :rtype: generator
        """
        sock = self.__sock(zmq.SUB)

        for topic in topics:
            if not isinstance(topic, bytes):
                error = 'Topics must be a list of bytes'
                log.error(error)
                raise TypeError(error)
            sock.setsockopt(zmq.SUBSCRIBE, topic)

        return self.__recv_generator(sock)

    # PushPull pattern
    def push(self):
        """
        Returns a callable that can be used to transmit a message in a push-pull
        fashion. Note that the sender function has a ``print`` like signature,
        with an infinite number of arguments. Each one being a part of the
        complete message.

        :rtype: function
        """
        sock = self.__sock(zmq.PUSH)
        return self.__send_function(sock)

    def pull(self):
        """
        Returns an iterable that can be used to iterate over incoming messages,
        that were pushed by a push socket. Note that the iterable returns as
        many parts as sent by pushers.

        :rtype: generator
        """
        sock = self.__sock(zmq.PULL)
        return self.__recv_generator(sock)

    # ReqRep pattern
    def request(self):
        """
        Returns a callable and an iterable respectively. Those can be used to
        both transmit a message and/or iterate over incoming messages,
        that were replied by a reply socket. Note that the iterable returns
        as many parts as sent by repliers. Also, the sender function has a
        ``print`` like signature, with an infinite number of arguments. Each one
        being a part of the complete message.

        :rtype: (function, generator)
        """
        sock = self.__sock(zmq.REQ)
        return self.__send_function(sock), self.__recv_generator(sock)

    def reply(self):
        """
        Returns a callable and an iterable respectively. Those can be used to
        both transmit a message and/or iterate over incoming messages,
        that were requested by a request socket. Note that the iterable returns
        as many parts as sent by requesters. Also, the sender function has a
        ``print`` like signature, with an infinite number of arguments. Each one
        being a part of the complete message.

        :rtype: (function, generator)
        """
        sock = self.__sock(zmq.REP)
        return self.__send_function(sock), self.__recv_generator(sock)

    # Pair pattern
    def pair(self):
        """
        Returns a callable and an iterable respectively. Those can be used to
        both transmit a message and/or iterate over incoming messages, that were
        sent by a pair socket. Note that the iterable returns as many parts as
        sent by a pair. Also, the sender function has a ``print`` like signature,
        with an infinite number of arguments. Each one being a part of the
        complete message.

        :rtype: (function, generator)
        """
        sock = self.__sock(zmq.PAIR)
        return self.__send_function(sock), self.__recv_generator(sock)

    def _setup(self, sock):
        raise NotImplementedError()

class Client(Sock):
    """
    A client that can connect to a set of servers.
    """
    def __init__(self):
        """
        Constructor of the Client.
        """
        self._sock = None
        self._is_ready = False
        self._addresses = []

        Sock.__init__(self)

    def _setup(self, sock):
        self._sock = sock
        self._is_ready = True

        _check_valid_num_connections(self._sock.socket_type,
                                     len(self._addresses))

        for ip, port in self._addresses:
            _connect_zmq_sock(self._sock, ip, port)

    @property
    def addresses(self):
        """
        Returns a tuple containing all the connected addresses. Each address
        is a tuple with an ip address and a port.

        :rtype: (addresses)
        """
        return tuple(self._addresses)

    def connect(self, ip, port):
        """
        Connects to a server at the specified ip and port.

        :param ip: an IP address
        :type ip: str or unicode
        :param port: port number from 1024 up to 65535
        :type port: int
        """
        _check_valid_port_range(port)

        address = (ip, port)

        if address in self._addresses:
            error = 'Already connected to {0} on port {1}'.format(ip, port)
            log.exception(error)
            raise ValueError(error)

        self._addresses.append(address)

        if self._is_ready:
            _check_valid_num_connections(self._sock.socket_type,
                                         len(self._addresses))

            _connect_zmq_sock(self._sock, ip, port)

    def connect_local(self, port):
        """
        Connects to a server in localhost at the specified port.

        :param port: port number from 1024 up to 65535
        :type port: int
        """
        self.connect('127.0.0.1', port)

    def disconnect(self, ip, port):
        """
        Disconnects from a server at the specified ip and port.

        :param ip: an IP address
        :type ip: str or unicode
        :param port: port number from 1024 up to 65535
        :type port: int
        """
        _check_valid_port_range(port)
        address = (ip, port)

        try:
            self._addresses.remove(address)
        except ValueError:
            error = 'There was no connection to {0} on port {1}'.format(ip, port)
            log.exception(error)
            raise ValueError(error)

        if self._is_ready:
            _disconnect_zmq_sock(self._sock, ip, port)

    def disconnect_local(self, port):
        """
        Disconnects from a server in localhost at the specified port.

        :param port: port number from 1024 up to 65535
        :type port: int
        """
        self.disconnect('127.0.0.1', port)

    def disconnect_all(self):
        """
        Disconnects from all connected servers.
        """
        addresses = deepcopy(self._addresses)

        for ip, port in addresses:
            self.disconnect(ip, port)

class Server(Sock):
    """
    A server that clients can connect to.
    """
    def __init__(self, port):
        """
        Constructor of the Server.

        :param port: port number from 1024 up to 65535
        :type port: int
        """
        _check_valid_port_range(port)
        self._port = port

        Sock.__init__(self)

    def _setup(self, sock):
        if sock.socket_type == zmq.SUB:
            warning = 'SUB sockets that bind will not get any message before '
            warning += 'they first ask for via the provided generator, so '
            warning += 'prefer to bind PUB sockets if missing some messages '
            warning += 'is not an option'
            warn(warning)

        _bind_zmq_sock(sock, self._port)

    @property
    def port(self):
        """
        Returns the port.

        :rtype: int
        """
        return self._port
