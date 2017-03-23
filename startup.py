#coding=utf-8

import functools
import socket

from tornado.log import access_log as logger
from tornado.options import options
import tornado.ioloop

from core.dispatcher.handler import Dispatcher,connection_ready
from core.scanner import Scanner
from core.initialize import get_global_config
from core.settings import TRACE_SERVICE_PATH,INSTRUCT_TASK_PATH,SOCKET_PORT,WEB_PORT

from web.main import load_web


#define('port')

def start():
    # 这里可能会配置log
    options.parse_command_line()
    #if options.port is None:
    #    logger.info("Start server fail, port is null")
    #    return

    # 必须先scan trace
    # 会载入所有根目录service目录下文件中
    # 使用@set_trace包裹的函数
    # 会验证trace名字的唯一性
    # 不通过验证会生成异常
    Scanner.scan_trace(TRACE_SERVICE_PATH)

    # 加载所有的 instruct
    # 会对所有instruct以及subtask的trace进行合法性验证
    # 会对所有重复的instruct名字进行验证
    # 不通过验证会生成异常
    Scanner.scan_instruct(INSTRUCT_TASK_PATH)

    # 生成golbal config 对象
    # 将扫描到的任务和trace全部加载到返回的配置对象中
    golbal_config = get_global_config(Scanner)

    host = ''
    port = int(SOCKET_PORT)

    core = Dispatcher.get_dispatcher(golbal_config)

    load_web('templates',WEB_PORT)

    # 这里参考tornado的手册
    # 可以换成http服务器
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind((host, port))
    sock.listen(128)

    io_loop = tornado.ioloop.IOLoop.current()

    # 将dispatcher赋给事件处理函数
    callback = functools.partial(connection_ready, sock,core)
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    logger.info("Socket server start, take port is: %s", port)
    logger.info("Web server start, take port is: %s", WEB_PORT)
    io_loop.start()


if __name__ == '__main__':
    #import sys
    #sys.argv.append('--port=7981')
    start()