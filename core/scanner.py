#coding=utf-8

import os
import importlib

from tornado.log import access_log as logger

from .utils.errors import CeQuantCoreError
from .interface import DataStream,CommandWord

def set_trace(trace_name):
    def func_wrapper(func):
        if trace_name in Scanner.trace_store:
            raise CeQuantCoreError('trace name %s allready exists' % trace_name)

        logger.info("\t|-- trace %s is adding to tracemap" % trace_name)

        # 对func的输入和输出进行检查
        # 搞不明白为什么这样使用会cannot pickle
        # 换个地方实现对输入输出的判断
        # def check_func(iostream,cmd):
        #    if not isinstance(iostream,DataStream):
        #        raise CeQuantCoreError('first argument of trace func %s must be instance of DataStream' % func.__name__)
        #    if not isinstance(cmd,CommandWord):
        #        raise CeQuantCoreError('second argument of trace func %s must be instance of CommandWord' % func.__name__)
        #    res = func(iostream,cmd)
        #    if not isinstance(res,DataStream):
        #        raise CeQuantCoreError('return obj of trace %s func must be instance of DataStream' % func.__name__)
        #    return res

        Scanner.trace_store[trace_name] = func
        return func
    return func_wrapper

def set_instruct(instruct_name):
    def func_wrapper(func):
        if instruct_name in Scanner.instruct_store:
            raise CeQuantCoreError('instruct name %s allready exists' % instruct_name)

        logger.info("\t|-- info of instruct %s is adding to instructmap" % instruct_name)
        instructinfo = func()
        instruct_trace = instructinfo.get_trace()
        if instruct_trace is not None:
            _check_trace_legal(instruct_trace,instructinfo.name)
        gettasks = instructinfo.get_task()
        for n in gettasks:
            subtrace = n.get('trace')
            if subtrace is not None:
                _check_trace_legal(subtrace,n['name'])
            elif instruct_trace is None and subtrace is None:
                raise CeQuantCoreError('instruct trace and subtrace must not be not set at the sametime')

        Scanner.instruct_store[instruct_name] = func()
        return func
    return func_wrapper

def _check_trace_legal(trace,name):
    prethread = trace.get('prethread')
    if prethread is not None and prethread not in Scanner.trace_store:
        raise CeQuantCoreError('task or instruct %s has a prethread named %s has not been registered' % (name,prethread))
    trace = trace.get('trace')
    if trace is not None:
        for n in trace:
            if n not in Scanner.trace_store:
                raise CeQuantCoreError('task or instruct %s has a trace node named %s has not been registered' % (name,n))
    return True



class Scanner:
    trace_store = {}
    instruct_store = {}
    _loaded_module = []
    _scaned = False

    @staticmethod
    def scan_path(modulepath):
        if not os.path.exists(modulepath):
            raise CeQuantCoreError('cannot find path %s' % modulepath)
        if not os.path.isdir(modulepath):
            raise CeQuantCoreError('path %s is not a dir name' % modulepath)
        if modulepath.endswith("/"):
            newpath = modulepath.replace("/", "")
        else:
            newpath = modulepath

        os.path.walk(newpath,Scanner.single_scan,newpath)

    @staticmethod
    def scan_trace(tracepath):
        logger.info("Begin Scan all trace services...")
        Scanner.scan_path(tracepath)

    @staticmethod
    def scan_instruct(tracepath):
        logger.info("Begin Scan all instructs...")
        Scanner.scan_path(tracepath)

    @staticmethod
    def single_scan(arg, dirname, names):
        modulepath = dirname.replace(os.path.sep,'.')
        for n in names:
            if (not n.startswith('__')) and n.endswith('.py'):
                subname = n.split('.')[0]
                importpath = '.'.join([modulepath,subname])
                Scanner._loaded_module.append(importlib.import_module(importpath))
        Scanner._scaned = True

    @staticmethod
    def get_tracemanger():
        if not Scanner._scaned:
            raise CeQuantCoreError('trace must be scaned before start')
        return Scanner.trace_store

    @staticmethod
    def clear():
        Scanner._scaned = False
        for n in Scanner.trace_store.keys():
            del Scanner.trace_store[n]
        for n in Scanner.instruct_store.keys():
            del Scanner.instruct_store[n]
        while Scanner._loaded_module:
            module = Scanner._loaded_module.pop(0)
            reload(module)





