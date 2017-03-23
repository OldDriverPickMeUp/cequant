#coding=utf-8

import threading
import traceback
from multiprocessing.pool import Pool

from tornado.log import access_log as logger

from .instruct import InstructManager
from .task import CoreTask,core_task_trace_parser

from ..utils.errors import CeQuantCoreError
from ..coreconfig import ConfigManager
from ..utils.wrapper import thread_lock
from ..lib.multiple.process.pool import MyPoolwithPipe
from ..settings import MAX_PARALLEL_PROCESS
from ..interface import DataStream,CommandWord
from ..utils.errors import CeQuantError,CeQuantTaskError


class TaskManager:
    _thread_lock = threading.Lock()

    def __init__(self, config):
        """
            MemCtrl对象的构造函数
        :param para: 有下面几个键
            config：字典对象有如下几个键：
                configpath：配置文件路径
                log：日志文件名
                getdata：获取数据函数
                get_backtest_data：获取回测任务的数据函数
            maxtask：最大并行任务数
            maxunempty：最大清理内存间隔
        """

        #初始化写必要的变量

        if not isinstance(config,ConfigManager):
            raise CeQuantCoreError('config must be instance of ConfigManager')

        self._instruct_manager = None




        #self._maxtask = MAX_PARALLEL_PROCESS
        self._tracemanager = config.get('tracemanager')

        #self._taskpool = MyPoolwithPipe(self._maxtask)
        self._taskpool = Pool(MAX_PARALLEL_PROCESS)
        self._activetask = 0
        self._maxactivetask = MAX_PARALLEL_PROCESS
        self._taskqueue = []

    def initialize(self,instruct_manager):
        if not isinstance(instruct_manager,InstructManager):
            raise CeQuantCoreError('instruct_manager should be instance of InstructManager')
        self._instruct_manager=instruct_manager


    def starttask(self,instruct,task,name,trace,params):
        #创建任务和线程
        #core_task = CoreTask(name)
        workthread=threading.Thread(target=self._worker,args=(instruct,task,trace,params))
        workthread.setDaemon(True)

        if self._activetask>=self._maxactivetask:
            self._taskqueue.append(workthread)
        else:
            self._activetask+=1
            workthread.start()
        #return True

    def _finishtask(self):
        with self._thread_lock:
            if len(self._taskqueue) != 0:
                nextthread = self._taskqueue.pop(0)
                nextthread.start()

    def _worker(self,instruct,task_id,trace,params):

        try:
            self._instruct_manager.start_task(instruct, task_id)
            # 解析trace
            pre_thread = trace.get('pre_thread', 'bypass')

            cmdword = CommandWord(params)
            istream = self._tracemanager.get(pre_thread)(DataStream(),cmdword)

            task = self._taskpool.apply_async(core_task_trace_parser,
                                              (self._tracemanager, istream, trace['trace'], cmdword))

            result = task.get()

        except CeQuantTaskError as e:
            logger.error(e.detail)
            result = {'code': 'ERROR', 'msg': e.detail}
        except CeQuantError as e:
            logger.error(e.get_format_error_info())
            result = {'code':'ERROR','msg':e.detail}
        except:
            errmsg = traceback.format_exc()
            result = {'code':'ERROR','msg':errmsg}
            logger.error(errmsg)



        if result['code']=='OK':
            self._instruct_manager.success(instruct, task_id)
        else:

            errstr = result['detail']
            self._instruct_manager.error(instruct, task_id, errstr)

        #返回数据
        #找到IOLOOP,add callback
        self._finishtask()


