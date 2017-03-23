#coding=utf-8

from threading import Lock

from .message import create_success_msg

def thread_lock(func):
    def innerfunc(*args,**kwargs):
        lck=Lock()
        lck.acquire()
        result = func(*args,**kwargs)
        lck.release()
        return result
    return innerfunc



def api_wrapper(func):
    def inner(kwargs):
        api=kwargs.get('api')
        if api:
            desc=func(kwargs)
            return create_success_msg('api_mode', desc)
        else:
            return create_success_msg(func(kwargs))
    return inner

