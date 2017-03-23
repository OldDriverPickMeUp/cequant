#coding=utf-8

import os

from tornado.web import Application

from .htmlhandlers import IndexHandler,HtmlHandler
from .apihandler import ApiHandler


def load_web(template,port):
    application = Application([
        (r'/', IndexHandler),
        (r'/(.*html)', HtmlHandler),
        (r"/api/(.*)", ApiHandler),
    ], template_path=os.path.join(os.getcwd(), 'web', template))
    application.listen(port)