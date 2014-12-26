import zmq

from time import sleep

def connect(port, ip='127.0.0.1'):
    return ConnectSock(ip, port)

def bind(port, interface='*'):
    return BindSock(interface, port)

class Sock:
    def __init__(self):
        self._sock = None
        self._context = zmq.Context()

    def __del__(self):
        if self._sock:
            self._sock.close()

    def __sock(self, pattern, sleepTime=0):
        if not self._sock:
            self._sock = self._context.socket(pattern)
            self._disable_patterns_except(pattern)
            self.setup()

            if pattern == zmq.SUB:
                self._sock.setsockopt(zmq.SUBSCRIBE, b'')
                sleep(5)
            elif pattern == zmq.PUB:
                sleep(5)

        return self._sock

    def __send(self, pattern, data):
        return self.__sock(pattern).send_multipart(data)

    def __recv(self, pattern):
        frames = self.__sock(pattern).recv_multipart()
        return frames if len(frames) > 1 else frames[0]

    def _disable_patterns_except(self, pattern):
        if not pattern == zmq.PUB: self.pub = None
        if not pattern == zmq.SUB: self.listen_for_pub = None
        if not pattern == zmq.PULL: self.listen_for_push = None
        if not pattern == zmq.PUSH: self.push = None
        if not pattern == zmq.REQ: self.request = None
        if not pattern == zmq.REP:
            self.reply = None
            self.listen_for_request = None
        if not pattern == zmq.PAIR:
            self.pair = None
            self.listen_for_pair = None

    def pub(self, *data):
        self.__send(zmq.PUB, data)

    def listen_for_pub(self):
        while True:
            yield self.__recv(zmq.SUB)

    def push(self, *data):
        self.__send(zmq.PUSH, data)

    def listen_for_push(self):
        while True:
            yield self.__recv(zmq.PULL)

    def request(self, *data):
        self.__send(zmq.REQ, data)
        return self.__recv(zmq.REQ)

    def listen_for_request(self):
        while True:
            yield self.__recv(zmq.REP)

    def reply(self, *data):
        self.__send(zmq.REP, data)

    def listen_for_pair(self):
        while True:
            yield self.__recv(zmq.PAIR)

    def pair(self, *data):
        self.__send(zmq.PAIR, data)

    def setup(self):
        raise NotImplementedError()

class ConnectSock(Sock):
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port

        Sock.__init__(self)

    def setup(self):
        self._sock.connect('tcp://' + self._ip + ':' + str(self._port))

class BindSock(Sock):
    def __init__(self, interface, port):
        self._interface = interface
        self._port = port

        Sock.__init__(self)

    def setup(self):
        self._sock.bind('tcp://' + self._interface + ':' + str(self._port))
