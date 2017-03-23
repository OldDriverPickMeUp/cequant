#coding=utf-8
import socket

from tornado.iostream import IOStream
from core.settings import SOCKET_PORT

class SocketConnection:
    def __init__(self,send_str,callback):
        self._stream = None
        self._host = 'localhost'
        self._port = SOCKET_PORT
        self._send_str = send_str
        self._callback = callback

    def _get_stream(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self._stream = IOStream(sock)

    def start_work(self):
        self._get_stream()
        self._stream.connect((self._host, self._port),self._send)

       # self._stream.read_bytes(2, self._finish)

    def _send(self):
        #print self._req._finished

        #print 'sadsa',self._send_str
        self._stream.write(self._send_str)

        #self._stream.read_until(self.EOF, self._finish)
        self._stream.read_until_close(self._finish)
        #print 'asddsaasd'


    def _finish(self,data):

        self._stream.close()
        self._callback(data.strip())
        #self._req._callback(data)
