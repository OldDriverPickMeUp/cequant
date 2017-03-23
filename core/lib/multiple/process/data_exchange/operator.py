#coding=utf-8
from .request import RequestExchange

class DataAcquire:
    """
    DataAcquire class is used to get data from father process in child process
    """

    def __init__(self, acq=None, rev=None):
        """
            数据获取类的构造函数
        :param acq: 获取方法
        :param rev: 接收方法
        """
        self._acq = acq
        self._rev = rev

    @staticmethod
    def _data_handler(obj, handlers=None):
        """
            数据处理器
        :param obj: 数据
        :param handlers:处理方法
        :return:
        """
        if not handlers:
            return obj
        else:
            return handlers[obj.head](obj.data)

    def _request(self, obj):
        """
            获得数据的内部方法
        :param obj: 交换数据对象
        :return:
        """
        # print '_req',obj
        self._acq(obj)

    def _receive(self, handlers=None):
        """
            接收数据的内部方法
        :param handlers: 数据处理的方法
        :return: 处理过的数据
        """
        data = self._data_handler(self._rev(), handlers)
        return data

    def getdata(self, handler=None, **para):
        """
            数据获取接口
        :param handler:处理器
        :param para: 构造请求数据类的参数
        :return: 需要接收的数据
        """
        self._request(RequestExchange(**para)())
        return self._receive(handler)

    def getdata_local(self, handler=None, **para):
        """
            本地的数据获取方法
        :param handler: 处理器
        :param para:  构造请求数据类的参数
        :return:
        """
        return RequestExchange(**para)()
