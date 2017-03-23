#coding=utf-8


from .utils.errors import CeQuantCoreError

# 这里定义了trace之间的交互类型
# trace的输入是数据流和控制字
class DataStream:
    def __init__(self,indict = None):
        if indict is None:
            self._data = {}
        elif isinstance(indict,dict):
            self._data = indict
        else:
            raise CeQuantCoreError('parameter indict must be instance of dict')
    def set(self,key,obj):
        self._data[key] = obj
    def get(self,key):
        obj = self._data.get(key)
        if obj is None:
            raise CeQuantCoreError('data with key %s does not exist in this object' % key)
        return obj
    def remove(self,key):
        if key not in self._data.keys():
            raise CeQuantCoreError('data with key %s does not exist in this object' % key)
        del self._data[key]

class CommandWord(DataStream):
    pass