#coding=utf-8

import multiprocessing

from multiprocessing.pool import Pool as BasePool
from multiprocessing.queues import SimpleQueue
from multiprocessing.util import debug

from .data_exchange.exchange import DataExchange
from .worker import myworker

class pooltask:
    def __init__(self,**para):
        self.task=para.get('task')
        if self.task==None:
            raise Exception('task cannot be None!')
        self.argsdict=para.get('argsdict')

class poolofworker:
    def __init__(self,config=None):

        self.config=config
        self.tasklist=[]

    def appendtask(self,task):

        if not isinstance(task,pooltask):
            raise Exception('appendtask must be inherited from class pooltask!')
        self.tasklist.append(task)

    def extendtask(self,tasklist):

        if type(tasklist)!=list:
            raise Exception('extendtask must be a list of tasks!')
        for task in tasklist:
            if not isinstance(task,pooltask):
                raise Exception('extendtask must be inherited from class pooltask!')
        self.tasklist.extend(tasklist)

    def dowithresults(self,res):

        pass

    def startwork(self,num_of_workers):

        if len(self.tasklist)==0:
            raise Exception('No Task in Batch Now!!You should use poolofworker.appendtask or poolofworker.extendtask to add task ')
        p=multiprocessing.Pool(num_of_workers)
        res=[]
        for task in self.tasklist:
            res.append(p.apply_async(task.task,(task.argsdict,)))
        p.close()
        p.join()
        results=[]
        for re in res:
            results.append(re.get())
        self.dowithresults(results)




class MyPoolwithPipe(BasePool):
    """
        带管道的进程池类，为每个进程额外添加了两个带锁的管道，可以时间双工的数据传输
    """

    def __init__(self, processes=None):
        """
            MyPoolwithPipe的构造函数
        :param processes: 最大进程数
        """
        BasePool.__init__(self, processes)

    def _setup_queues(self):
        """
            设定用于通信的SimpleQueue
        :return:
        """
        BasePool._setup_queues(self)
        self._get_data_queue = SimpleQueue()
        self._require_data_queue = SimpleQueue()

    def _repopulate_pool(self):
        """Bring the number of pool processes up to the specified number,
        for use after reaping workers which have exited.
        """
        for i in range(self._processes - len(self._pool)):
            w = self.Process(target=myworker,
                             args=(self._inqueue, self._outqueue,
                                   self._initializer,
                                   self._initargs, self._maxtasksperchild,
                                   self._require_data_queue,
                                   self._get_data_queue)
                             )
            self._pool.append(w)
            w.name = w.name.replace('Process', 'PoolWorker')
            w.daemon = True
            w.start()
            debug('added worker')

    def send_data(self, data):
        """
            向管道传送数据
        :param data: 数据交换类的初始化字典
        :return:
        """
        self._get_data_queue.put(DataExchange(data['head'], data['data'])())

    def get_data(self):
        """
            获得进程池内进程的数据请求
        :return: 请求的数据
        """
        return self._require_data_queue.get()

    def set_stop(self):
        """
            关闭数据服务进程
        :return:
        """
        self._require_data_queue.put(-1)