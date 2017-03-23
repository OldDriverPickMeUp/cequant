#coding=utf-8

class DataExchange:
    """
    data exchange object is the recived data type from father process,each object has a head as a tag to data obj
    """
    def __init__(self, head, data):
        """
            DataExchange类的构造函数
        :param head: 数据头
        :param data: 数据体
        """
        self.head=head
        self.data=data

    def __call__(self):
        """
            DataExchange类的__call__方法
        :return: 字典数据
        """
        return {'head':self.head,
                'data':self.data}


