#coding=utf-8

import simplejson

from .errors import CeQuantCoreError

class MessageManager:
    def __init__(self, status, msg):
        self.status = status
        self.msg = msg
        self.responce = {}

    def push_data(self, key, value):
        self.responce.__setitem__(key, value)
        return self

    def push_all(self, dictObj):
        if not isinstance(dictObj, dict):
            raise CeQuantCoreError("Param: dictObj is not a dict")

        self.responce.update(dictObj)
        return self

    def set_msg(self,msg):
        self.msg=msg
        return self

    def out(self):
        return simplejson.dumps(self.__dict__)


def create_success_msg(msg='',responce={}):
    msgobj = MessageManager("success", msg)
    if responce:
        msgobj.push_all(responce)
    return msgobj

def create_error_msg(msg,responce={}):
    msgobj = MessageManager("error", msg)
    if responce:
        msgobj.push_all(responce)
    return msgobj


def create_msg(status,msg):
    return MessageManager(status,msg)



