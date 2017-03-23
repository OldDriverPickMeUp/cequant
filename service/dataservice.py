#coding=utf-8

import pandas as pd
from tornado.log import access_log as logger

from core.datahandler.datastore import DataStore

from .const import DATA_EXCHANGE_DATE_KEY,DATA_BASIC_STOCK_KEY,DATA_FILTER_KEYS,\
    DATA_STOCK_LIMIT_DOWN_KEY,DATA_STOCK_LIMIT_UP_KEY,DATA_STOCK_SUSPENSION_KEY,\
    DATA_STOCK_AFCLOSE_KEY,DATA_STOCK_AFOPEN_KEY

class DataManager:
    def __init__(self,starttime,endtime):
        self._datastore = DataStore()
        self._outputdict = {}
        self._start = starttime
        self._end = endtime

    def stock_info(self):       #交易日、基本信息
        df = self._datastore.get_resource_by_key(DATA_EXCHANGE_DATE_KEY)
        df = df.loc[df[0] == 1]
        self._outputdict['exchange_date'] = df.ix[self._start:self._end]
        self._outputdict['basicstock'] = self._datastore.get_resource_by_key(DATA_BASIC_STOCK_KEY)
        return self

    def stock_price(self):      #股票价格
        self._outputdict['open'] = self._datastore.get_resource_by_key(DATA_STOCK_AFOPEN_KEY)[0].ix[self._start:self._end]
        self._outputdict['close'] = self._datastore.get_resource_by_key(DATA_STOCK_AFCLOSE_KEY)[0].ix[self._start:self._end]
        return self

    def single_stock_price(self,symbol):  # 股票价格
        pass

    def index_price(self,symbol):      #指数价格
        pass

    def load_factor_timming(self,factor_ids,timming_ids,weights=None,directions=None):       #打分数据
        if weights is None:     #生成默认权重
            factor_weight = []
            cls = []
            for n in factor_ids:
                cls.append(int(n / 100))
                factor_weight.append(1.)
            cls_cnt = len(set(cls))
            for n in range(len(cls)):
                factor_weight[n] = factor_weight[n] / cls.count(cls[n]) / cls_cnt
        else:
            factor_weight = weights

        if directions is None:   #生成默认方向，全部正向
            factor_direction = [1.] * len(factor_ids)
        else:
            factor_direction = directions

        assert len(factor_direction) == len(factor_weight)
        for n in range(len(factor_direction)):
            factor_weight[n]=factor_weight[n]*factor_direction[n]
        factor_weight.extend([1.]*len(DATA_FILTER_KEYS))
        factor_df = self._datastore.get_cache_by_ids(factor_ids,DATA_FILTER_KEYS).ix[self._start:self._end]
        self._outputdict['factor'] = factor_df
        self._outputdict['weight'] = factor_weight

        #生成描述
        factorname = [self._datastore.get_desc_by_id(id) for id in factor_ids]
        data = {'weight':factor_weight,
                'direction':factor_direction}
        factor_df = pd.DataFrame(index = factorname,data=data)
        self._outputdict['factor_description'] = factor_df
        return self

    def load_timming(self,timming_ids):
        self._outputdict['timming'] = [self._datastore.get_resource_by_id(id).ix[:self.end] for id in timming_ids]
        timmingname = [self._datastore.get_resource_by_id(id) for id in timming_ids]
        self._outputdict['timming_description'] = timmingname
        return self

    def stock_status(self):         #停牌等
        self._outputdict['stock_limitup'] = self._datastore.get_resource_by_key(DATA_STOCK_LIMIT_UP_KEY)[0]
        self._outputdict['stock_limitdown'] = self._datastore.get_resource_by_key(DATA_STOCK_LIMIT_DOWN_KEY)[0]
        self._outputdict['stock_suspension'] = self._datastore.get_resource_by_key(DATA_STOCK_SUSPENSION_KEY)[0]
        return self

    def output(self):
        return self._outputdict