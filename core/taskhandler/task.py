#coding=utf-8

import time
import sys
import traceback

from ..utils.errors import CeQuantCoreError,CeQuantTaskError,CeQuantError
from ..interface import DataStream,CommandWord

class CoreTask:

    def __init__(self,name):
        self._name = name
        self._status = 'halt'
        self._starttime = None
        self._runtime = 0.
        self._errormsg = ''

    def start(self):
        self._starttime=time.time()
        self._status='running'

    def finish(self):
        self._status='finished'
        self._runtime=time.time()-self._starttime

    def error(self,errormsg):
        self._status = 'error'
        self._errormsg = errormsg
        self._runtime = time.time()-self._starttime

    def getstatus(self):
        return {'name':self._name,
                'running time':'%.2f s' % self._runtime,
                'status':self._status,
                'message':self._errormsg}


class InstrcutInfo:
    def __init__(self,name):
        self._taskinfo = []
        self.trace = None
        self.name = name

    def add_task(self,taskinfo):
        if not isinstance(taskinfo,TaskInfo):
            raise CeQuantCoreError('taskinfo must be instance of TaskInfo')
        self._taskinfo.append(taskinfo)
        return self

    def set_trace(self,tasktrace):
        if not isinstance(tasktrace,dict):
            raise CeQuantCoreError('tasktrace must be instance of TaskTrace')
        self.trace=tasktrace
        return self

    def get_task(self):
        if not self._taskinfo:
            return [TaskInfo(self.name)]
        return self._taskinfo

    def get_trace(self):
        return self.trace

class TaskInfo(dict):
    def __init__(self,name,trace=None):
        self['name']=name
        if trace:
            self['trace']=trace

    def set_trace(self, tasktrace):
        if not isinstance(tasktrace, dict):
            raise CeQuantCoreError('tasktrace must be instance of TaskTrace')
        self['trace'] = tasktrace
        return self


class TraceMaker:
    def __init__(self):
        self._trace = {'trace': []}

    def set_prethread(self, tracename):
        self._trace['prethread'] = tracename
        return self

    def add_node(self, key):
        if not isinstance(key, str) and not isinstance(key, list):
            raise CeQuantCoreError('single trace node key must be str or list of str')
        self._trace['trace'].append(key)
        return self

    def get_trace(self):
        return self._trace



def core_task_trace_parser(tracemanager,istream,trace,params):
    try:
        if not isinstance(istream,DataStream):
            raise CeQuantTaskError('core taak input argument must be instance of DataStream')
        stream=istream
        for n in trace:
            if not isinstance(n,list):
                stream=tracemanager.get(n)(stream,params)
                if not isinstance(stream,DataStream):
                    raise CeQuantTaskError('return value of trace %s must be instance of DataStream' % n)
            else:
                tmp_stream=[]
                for m in n:
                    stream = tracemanager.get_function(m)(stream, params)
                    if not isinstance(stream, DataStream):
                        raise CeQuantTaskError('return value of trace %s in trace node %s must be instance of DataStream' % (m,n))
                    tmp_stream.append(stream)
                stream=tracemanager.merge(tmp_stream)
        return {'code':'OK','msg':'finished'}
    except CeQuantError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        errlines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        errmsg = ''.join(errlines)
        return {'code':'ERROR','msg':e.detail,'detail':errmsg}
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        errlines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        errmsg = ''.join(errlines)
        return {'code':'UNKNOWN ERROR','msg':e.message,'detail':errmsg}


def merge(inlist):
    outstream=[]
    for n in inlist:
        if n!=0:
            outstream.append(n)
    if len(outstream)==0:
        return 0
    elif len(outstream)==1:
        return outstream[0]
    else:
        return outstream


