#coding=utf-8

import time

import simplejson

from tornado.ioloop import IOLoop

from dev.socketconn import SocketConnection
from core.settings import SOCKET_EOF

CONTROLLER_MAP = {}

def check(request,callback):
    page = request.get_argument('page')
    #print page
    conn = SocketConnection(simplejson.dumps({'taskname':'check','page':int(page)})+SOCKET_EOF,callback)
    conn.start_work()
CONTROLLER_MAP['/api/check']=check


def getsubtask(request,callback):
    instruct_id = request.get_argument('instruct_id')
    conn = SocketConnection(simplejson.dumps({'taskname': 'get_subtask', 'instruct_id': instruct_id}) + SOCKET_EOF, callback)
    conn.start_work()
CONTROLLER_MAP['/api/getsubtask'] = getsubtask

def echo(request,callback):

    IOLoop.current().add_timeout(time.time()+5,callback,'this is an echo')
CONTROLLER_MAP['/api/echo'] = echo
