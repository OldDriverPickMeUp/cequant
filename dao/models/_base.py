#coding=utf-8

from core.utils.errors import CeQuantDBError



class TableModol:
    _columns = ()
    _types = ()
    db = {}
    filename = ''
    sql = ''
    def __init__(self):
        if len(self._columns) != len(self._types):
            raise CeQuantDBError('columns and types of %s have different length' % self.__class__)
        self._length = len(self._columns)
    def __getitem__(self, item):
        if not isinstance(item,int):
            raise Exception('getitem input item must be integer')
        if item>=self._length or item<0:
            raise Exception('item over ranges')
        return self._columns[item],self._types[item]

