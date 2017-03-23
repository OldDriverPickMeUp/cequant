#coding=utf-8

import time
import threading

from tornado.ioloop import IOLoop

from ..coreconfig import ConfigManager
from ..utils.errors import CeQuantCoreError,CeQuantInputError
from ..utils.generators import IdGenerator
from ..utils.message import create_success_msg,create_error_msg
from ..utils.wrapper import thread_lock
from ..settings import INSTRUCT_MAX_ITEMS_PAGE
from .task import CoreTask


class Instruction:
    """
        指令类（Instruction）是用来记录任务指令运行状况的对象，它会收集当前指令下
    所有任务的执行状况。可以根据当前指令的状况变化去触发一些新的任务或者指令。
    """
    def __init__(self,name,receipt,id,callback,conn):
        """
            指令对象的构造函数
        :param para: 为一个字典有如下键：
            instruction:指令名，instruction name，必须
            cmd：该指令的cmd信息，非必须，目前尚未使用
        """
        self._name = name
        self._receipt = receipt
        self._id = id
        self._callback = callback
        self._conn = conn
        self._subtasks=[]
        self._status='on'
        self._starttime=0
        self._runtime=0
        self._alltask=0
        self._finished=0

    def gather(self,subtask):
        """
            gather函数用来收集当前指令的子任务
        :param subtaskname: 子任务名称
        :param receipt:回执，希望是一个整形数据，目前并没有强制，默认-1
        :return:
        """
        self._subtasks.append(subtask)
        self._alltask+=1

    def error(self,task_id,errmsg):
        """
            将子任务设置为错误状态，该函数会在任务监视线程返回错误信息后，将子任务
        状态设置为错误状态
        :param taskname: 子任务的任务名
        :return:
        """
        self._subtasks[task_id].error(errmsg)
        self._finished+=1
        if self._finished>=self._alltask:
            self._runtime=(time.time()-self._starttime)/60
            self._status='error'
            self._onerror()

    def finish(self,task_id):
        """
            将子任务设置为成功状态，该函数会在任务监视线程正常返回时调用，将子任务
        状态设置为完成状态
        :param taskname: 子任务的任务名
        :return:
        """
        self._subtasks[task_id].finish()
        self._finished+=1
        if self._finished>=self._alltask:
            self._runtime=(time.time()-self._starttime)/60
            if self._status!='error':
                self._status='finished'
                self._onfinish()

    def start(self,task_id):
        self._subtasks[task_id].start()
        self._status = 'running'
        self._starttime=time.time()

    def isfinished(self):
        if self._status=='finished':
            return True
        else:
            return False

    def getstatus(self):
        """
            得到当前指令的状态，包括指令名，指令回执，指令已结束命令数，全部命令数，
        指令状态和已经运行时间
        :return: 表示指令状态的字符串
        """
        if self._status!='finished' and self._status!='error':
            self._runtime=(time.time()-self._starttime)/60
        return {'id':self._id,
                'taskname':self._name,
                'receipt':self._receipt,
                'rate of process':'%.2f %s'% (100.*self._finished/self._alltask,'%'),
                'status':self._status,
                'running time':'%.2f' % self._runtime}


    def getsubstatus(self):
        """
            得到当前指令所有子任务的状态，包括指令名，已完成数量，全部子任务，和指令
        状态。
        :return:表示指令信息和所有子任务信息的字符串
        """
        output=[]
        for n in self._subtasks:
            output.append(n.getstatus())
        return output

    def _onerror(self):
        msgobj = create_error_msg('error occurs in instruct %s ' % self._name,{'type':'return on finish'})
        currloop = IOLoop.instance()
        currloop.add_callback(self._callback,self._conn,msgobj.out())

    def _onfinish(self):
        msgobj = create_success_msg('successfully excute instruct %s' % self._name, {'type': 'return on finish'})
        currloop = IOLoop.instance()
        currloop.add_callback(self._callback, self._conn, msgobj.out())





class InstructManager:
    _thread_lock = threading.Lock()

    def __init__(self,config):
        if not isinstance(config,ConfigManager):
            raise CeQuantCoreError('config should be instance of ConfigManager')

        #self.config = config
        self.taskmanager = None
        self.id_generator = IdGenerator()

        self.instructions = {}
        self.instuct_list = []

        self.instuct_info = config.get('instruct_info')

    def initialize(self,taskmanager):
        self.taskmanager = taskmanager

    def handle(self,instructname ,cmd, callback, conn):

        instruct_info = self.instuct_info.get(instructname)
        if instruct_info is None:
            raise CeQuantInputError('instruct name does not exist')

        try:
            receipt = cmd['receipt']
        except:
            raise CeQuantInputError('task request need a receipt')

        instruct_id = self.id_generator.next()
        subtask_id = 0
        instruct = Instruction(name= instructname,receipt=receipt,id=instruct_id,callback=callback,conn = conn)
        self.add_instruct(instruct_id, instruct)
        instruct_trace = instruct_info.get_trace()
        for taskinfo in instruct_info.get_task():
            subtask_name = taskinfo['name']
            subtask_trace = taskinfo.get('trace')
            if subtask_trace is None:
                subtask_trace = instruct_trace
            instruct.gather(CoreTask(subtask_name))
            subtask = self.taskmanager.starttask(instruct=instruct_id,task=subtask_id,trace=subtask_trace,params=cmd,name=subtask_name)
            subtask_id+=1

        msgobj = create_success_msg('successfully build instruct',{'id':instruct_id})
        return msgobj

    def error(self,instruct_id,subtask_id,msg):
        with self._thread_lock:
            self.instructions[instruct_id].error(subtask_id,msg)

    def success(self,instruct_id,subtask_id):
        with self._thread_lock:
            self.instructions[instruct_id].finish(subtask_id)

    # 接口/操作函数
    def clean_instruct(self):
        with self._thread_lock:
            for n in self.instructions.keys():
                if self.instructions[n].isfinished():
                    del self.instructions[n]
        return {'executemsg':'finished instructions have been successfully cleaned'}


    # 接口/查询函数
    def get_instruct(self,page=0):
        outlist = []
        with self._thread_lock:
            if page<0:
                raise CeQuantInputError('page should be a none negetive integer')
            show_keys=sorted(self.instructions.keys(), reverse=True)[page*INSTRUCT_MAX_ITEMS_PAGE:(page+1)*INSTRUCT_MAX_ITEMS_PAGE]
            for n in show_keys:
                outlist.append(self.instructions[n].getstatus())
        return {'instructlist':outlist}


    # 接口/查询函数
    def get_subtask(self,instruct_id):
        instruct = self.instructions.get(instruct_id)
        if instruct is None:
            raise CeQuantInputError('instruct_id does not exists')
        return {'subtasks':instruct.getsubstatus()}

    def add_instruct(self,id,instruct):
        with self._thread_lock:
            self.instructions[id]=instruct

    def start_task(self,instruct_id,task_id):
        self.instructions[instruct_id].start(task_id)







