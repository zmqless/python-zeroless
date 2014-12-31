import zmq
import logging

from time import sleep
from warnings import warn
from functools import partial

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

def connect(port, ip='127.0.0.1'):
    return ConnectSock(ip, port)

def bind(port, interface='*'):
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
            sock.send_multipart(data)
            log.debug('Sending: {0}'.format(data))

    def __send_with_prefix(self, sock, prefix_frames):
        while True:
            data = prefix_frames + (yield)
            sock.send_multipart(data)
            log.debug('Sending: {0}'.format(data))

    def __recv(self, sock):
        while True:
            frames = sock.recv_multipart()
            log.debug('Receiving: {0}'.format(frames))
            yield frames if len(frames) > 1 else frames[0]

    def send_generator(self, sock, topic=None):
        if topic:
            gen = self.__send_with_prefix(sock, topic)
        else:
            gen = self.__send(sock)

        gen.send(None)
        func = lambda sender, *data: sender(data)
        return partial(func, gen.send)

    def recv_generator(self, sock):
        return self.__recv(sock)

    # PubSub pattern
    def pub(self, topic=b''):
        sock = self.__sock(zmq.PUB)
        return self.send_generator(sock, (topic,))

    def sub(self, topics=(b'',)):
        sock = self.__sock(zmq.SUB)

        for topic in topics:
            sock.setsockopt(zmq.SUBSCRIBE, topic)

        return self.recv_generator(sock)

    # PushPull pattern
    def push(self):
        sock = self.__sock(zmq.PUSH)
        return self.send_generator(sock)

    def pull(self):
        sock = self.__sock(zmq.PULL)
        return self.recv_generator(sock)

    # ReqRep pattern
    def request(self, *data):
        sock = self.__sock(zmq.REQ)
        return self.send_generator(sock), self.recv_generator(sock)

    def reply(self):
        sock = self.__sock(zmq.REP)
        return self.send_generator(sock), self.recv_generator(sock)

    # Pair pattern
    def pair(self, *data):
        sock = self.__sock(zmq.PAIR)
        return self.send_generator(sock), self.recv_generator(sock)

    def setup(self):
        raise NotImplementedError()

class ConnectSock(Sock):
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port

        Sock.__init__(self)

    def _setup(self, sock):
        log.info('Connecting to {0} on port {1}'.format(self._ip,
                                                        self._port))
        sock.connect('tcp://' + self._ip + ':' + str(self._port))

class BindSock(Sock):
    def __init__(self, interface, port):
        self._interface = interface
        self._port = port

        Sock.__init__(self)

    def _setup(self, sock):
        if sock.socket_type == zmq.SUB:
            warning = 'SUB sockets that bind will not get any message before '
            warning += 'they first ask for via the provided generator, so '
            warning += 'prefer to bind PUB sockets if missing some messages '
            warning += 'is not an option'
            warn(warning)

        log.info('Binding to interface {0} on port {1}'.format(self._interface,
                                                               self._port))
        sock.bind('tcp://' + self._interface + ':' + str(self._port))
