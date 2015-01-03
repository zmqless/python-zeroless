"""
The Zeroless module API.

.. data:: log

A global Logger object. To use it, just add an Handler object
and set an appropriate logging level.
"""

import zmq
import logging

from time import sleep
from warnings import warn
from functools import partial

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

def _check_valid_port_range(port):
    if port < 1024 or port > 65535:
        error = 'Port {0} is invalid, choose one between 1024 and 65535'
        error = error.format(port)
        raise ValueError(error)

def connect(port, ip='127.0.0.1'):
    """
    Returns a connector socket object.

    :param port: port number from 1024 up to 65535
    :type port: int
    :param ip: ip address to connect (default=127.0.0.1)
    :type ip: str or unicode
    :rtype: ConnectSock
    """
    return ConnectSock(ip, port)

def bind(port, interface='*'):
    """
    Returns a binding socket object.

    :param port: port number from 1024 up to 65535
    :type port: int
    :param interface: interface to bind (default=*)
    :type interface: str or unicode
    :rtype: BindSock
    """
    return BindSock(interface, port)

class Sock:
    def __init__(self):
        pass

    def __sock(self, pattern):
        sock = zmq.Context().instance().socket(pattern)
        self._setup(sock)

        log.info('Ready...')

        return sock

    def __send(self, sock):
        while True:
            data = (yield)
            log.debug('Sending: {0}'.format(data))

            try:
                sock.send_multipart(data)
            except TypeError:
                raise TypeError('Data must be bytes. Create another socket '
                                'and try again.')

    def __send_with_prefix(self, sock, prefix_frames):
        while True:
            data = prefix_frames + (yield)
            log.debug('Sending: {0}'.format(data))

            try:
                sock.send_multipart(data)
            except TypeError:
                raise TypeError('Data must be bytes. Create another socket '
                                'and try again.')

    def __recv(self, sock):
        while True:
            frames = sock.recv_multipart()
            log.debug('Receiving: {0}'.format(frames))
            yield frames if len(frames) > 1 else frames[0]

    def __send_function(self, sock, topic=None):
        if topic:
            gen = self.__send_with_prefix(sock, topic)
        else:
            gen = self.__send(sock)

        gen.send(None)
        func = lambda sender, *data: sender(data)
        return partial(func, gen.send)

    def __recv_generator(self, sock):
        return self.__recv(sock)

    # PubSub pattern
    def pub(self, topic=b''):
        """
        Returns a callable that can be used to transmit a message, with a given
        ``topic``, in a publisher-subscriber fashion. Note that the sender
        function has a ``print`` like signature, with an infinite number of
        arguments. Each one being a part of the complete message.

        :param topic: the topic that will be published to (default=b'')
        :type topic: bytes
        :rtype: function
        """
        if not isinstance(topic, bytes):
            raise TypeError('Topic must be bytes')

        sock = self.__sock(zmq.PUB)
        return self.__send_function(sock, (topic,))

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
                raise TypeError('Topics must be bytes')
            sock.setsockopt(zmq.SUBSCRIBE, topic)

        return self.__recv_generator(sock)

    # PushPull pattern
    def push(self):
        """
        Returns a callable that can be used to transmit a message in a push-pull
        fashion. Note that the sender function has a ``print`` like signature,
        with an infinite number of arguments. Each one being a part of the
        complete message.

        :rtype: a function
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
    def request(self, *data):
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
    def pair(self, *data):
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

class ConnectSock(Sock):
    """
    A socket that will connect to a binding socket.
    """
    def __init__(self, ip, port):
        """
        Constructor of the connector socket.

        :param port: port number from 1024 up to 65535
        :type port: int
        :param ip: ip address to connect
        :type ip: str or unicode
        """
        self._ip = ip
        self._port = port

        Sock.__init__(self)

    def _setup(self, sock):
        _check_valid_port_range(self._port)

        log.info('Connecting to {0} on port {1}'.format(self._ip,
                                                        self._port))
        sock.connect('tcp://' + self._ip + ':' + str(self._port))

class BindSock(Sock):
    """
    A socket that will bind for others to connect.
    """
    def __init__(self, interface, port):
        """
        Constructor of the binder object.

        :param port: port number from 1024 up to 65535
        :type port: int
        :param interface: interface to bind
        :type interface: str or unicode
        """
        self._interface = interface
        self._port = port

        Sock.__init__(self)

    def _setup(self, sock):
        _check_valid_port_range(self._port)

        if sock.socket_type == zmq.SUB:
            warning = 'SUB sockets that bind will not get any message before '
            warning += 'they first ask for via the provided generator, so '
            warning += 'prefer to bind PUB sockets if missing some messages '
            warning += 'is not an option'
            warn(warning)

        log.info('Binding to interface {0} on port {1}'.format(self._interface,
                                                               self._port))

        try:
            sock.bind('tcp://' + self._interface + ':' + str(self._port))
        except zmq.ZMQError:
            error = 'Port {0} is already in use'.format(self._port)
            raise ValueError(error)
