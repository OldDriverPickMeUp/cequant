#coding=utf-8

import socket
import errno
import traceback
import time
import threading
from functools import partial

import simplejson
from tornado.log import access_log as logger

from ..coreconfig import ConfigManager
from ..utils.errors import CeQuantCoreError,CeQuantError
from ..utils.message import create_error_msg,create_success_msg
from ..settings import SOCKET_EOF,SOCKET_TIMEOUT

from ..taskhandler.instruct import InstructManager
from ..taskhandler.interface import TaskManager

from .cmd import CommandManager

from tornado.iostream import IOStream
from tornado.ioloop import IOLoop



def connection_ready(sock,core,fd,event):
    """
    handler of socket connection
    """
    #print 'in'
    while True:
        try:
            connection,address=sock.accept()
        except socket.error as e:
            if e.args[0] not in (errno.EWOULDBLOCK,errno.EAGAIN):
                raise
            return

        # 保证能接收到
        # 从localhost接收数据会在事件到来之前产生
        #connection.settimeout(2)
        stream = IOStream(connection)
        stream.read_until(SOCKET_EOF,partial(handle,stream))
        return

def timeout_handler(stream,getstr):
    if stream.closed():
        return
    else:
        try:
            stream.write(create_error_msg('unknown error').out())
            stream.write(SOCKET_EOF)
            stream.close()
            logger.warning('%s request timeout' % getstr)
        except:
            stream.close(exc_info=True)

def handle(stream,data):
    #print data
    getstr = data.strip()
    mainioloop = IOLoop.current()
    mainioloop.add_timeout(time.time() + SOCKET_TIMEOUT, timeout_handler, stream,getstr)
    core = Dispatcher.get_dispatcher()
    core.handle(getstr,stream)

# 使用这个函数给最终返回信息
def callback(stream,sendstr):
    #print sendstr
    if stream.closed():
        return
    try:
        stream.write(sendstr)
        stream.write(SOCKET_EOF)
        stream.close()
    except:
        stream.close(exc_info=True)



class Dispatcher:
    dispatcher = None

    @classmethod
    def get_dispatcher(cls,config = None):
        return cls.instance(config)

    @classmethod
    def instance(cls,config = None):
        if cls.dispatcher is None:
            with threading.Lock():
                if cls.dispatcher is None:
                    cls.dispatcher = cls()
                    cls.dispatcher.initialize(config)
        return cls.dispatcher

    def initialize(self, config):

        if not isinstance(config,ConfigManager):
            raise CeQuantCoreError('config object must be instance of ConfigManager')

        # taskmanager 为任务执行提供了任务池并维护
        # instructmanager 是对指令进行解析，拆分成为任务集，并将单个任务分配给taskmanager的
        # instructmanager 会收集所有指令，以及每个指令的子任务的执行状况，
        # 栈追踪的结果等等，可以通过调度器的命令访问instructmanager内的数据
        self.taskmanager = TaskManager(config.get('taskmanager'))
        self.instructmanager = InstructManager(config.get('instructmanager'))

        self.instructmanager.initialize(self.taskmanager)
        self.taskmanager.initialize(self.instructmanager)

        #初始化所有的命令
        self.cmdmanager = CommandManager(self)
        self.cmdmanager.initialize()

    def handle(self, string, connection):
        """
        used to find which function will be called due to command string
        """

        try:
            cmd = simplejson.loads(string)
        except Exception:
            raise CeQuantCoreError('can not parse import json',trace=True)
        taskname = cmd.get('taskname', 'None')
        immediately = cmd.get('immediately')
        if immediately is None:
            immediately = False
        else:
            immediately = True
        if taskname:
            if self.cmdmanager.hascmd(taskname):
                try:
                    resobj=self.cmdmanager.excute(taskname,cmd)
                    msgobj = create_success_msg('%s successfully executed' % taskname,resobj)
                except CeQuantError as e:
                    logger.error(e.get_format_error_info())
                    msgobj = create_error_msg(e.detail, e.err_source)
                except:
                    logger.error(traceback.format_exc())
                    msgobj = create_error_msg('unknown error')
                finally:
                    callback(connection,msgobj.out())
                    return
            else:
                try:
                    msgobj = self.instructmanager.handle(taskname,cmd,callback,connection)
                except CeQuantError as e:
                    logger.error(e.get_format_error_info())
                    msgobj = create_error_msg(e.detail, e.err_source)
                    callback(connection, msgobj.out())
                except:
                    logger.error(traceback.format_exc())
                    msgobj = create_error_msg('unknown error')
                    callback(connection, msgobj.out())
                else:
                    if immediately:
                        callback(connection,msgobj.out())
                    return
        else:
            msgobj = create_error_msg('no such taskname')
            callback(connection, msgobj.out())
            return

