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
            sleep(sleepTime)

        return self._sock

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

    def pub(self, *data, sleepTime=5):
        self.__sock(zmq.PUB, 5).send_multipart(data)

    def listen_for_pub(self, sleepTime=5):
        sock = self.__sock(zmq.SUB, 5)
        sock.setsockopt(zmq.SUBSCRIBE, b'')

        while True:
            frames = sock.recv_multipart()
            yield frames if len(frames) > 1 else frames[0]

    def push(self, *data):
        self.__sock(zmq.PUSH).send_multipart(data)

    def listen_for_push(self):
        sock = self.__sock(zmq.PULL)

        while True:
            frames = sock.recv_multipart()
            yield frames if len(frames) > 1 else frames[0]

    def request(self, *data):
        sock = self.__sock(zmq.REQ)

        sock.send_multipart(data)
        frames = sock.recv_multipart()
        return frames if len(frames) > 1 else frames[0]

    def listen_for_request(self):
        sock = self.__sock(zmq.REP)

        while True:
            frames = sock.recv_multipart()
            yield frames if len(frames) > 1 else frames[0]

    def reply(self, *data):
        self.__sock(zmq.REP).send_multipart(data)

    def listen_for_pair(self):
        sock = self.__sock(zmq.PAIR)

        while True:
            frames = sock.recv_multipart()
            yield frames if len(frames) > 1 else frames[0]

    def pair(self, *data):
        self.__sock(zmq.PAIR).send_multipart(data)

    def setup(self):
        raise NotImplemented()

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
