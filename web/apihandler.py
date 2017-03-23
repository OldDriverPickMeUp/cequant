#coding=utf-8

import traceback
import simplejson
from tornado.web import RequestHandler,asynchronous
from tornado.log import access_log as logger
from .controller import CONTROLLER_MAP
from tornado.stack_context import wrap

class ApiHandler(RequestHandler):

    @asynchronous
    def get(self,*args,**kwargs):
        req_path = self.request.path
        func = CONTROLLER_MAP.get(req_path)
        if func is None:
            self.send_error(404)
            self.finish()
            return
        try:
            func(self,self._callback)
        except:
            logger.error(traceback.print_exc())
            self.send_error(500)
            if not self._finished:
                self.finish()

    def _callback(self,data):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        #print data

        self.write(data)
        #self.write(simplejson.loads(data))
        #print self._finished
        self.finish()
        #self.write('dsasad')

    def post(self,*args,**kwargs):
        self.get(*args,**kwargs)

