#coding=utf-8

import os
import datetime

import pandas as pd
from tornado.log import access_log as logger

from ..settings import DATA_BASE_PATH
from ..coreconfig import ConfigManager
from ..utils.errors import CeQuantCoreError,CeQuantInputError

__all__ = ['DataStore']

class DataStore:
    _datadict = {}
    _cachedf = None
    _resourcemap = None
    _preloadkeys = None
    _preloadids = None
    _id_key_map = None
    _lastloadtime = None
    _lastdatatime = None

    @staticmethod
    def initialize(config):
        if not isinstance(config,ConfigManager):
            raise CeQuantCoreError('config must be instance of ConfigManager')
        DataStore._resourcemap = config.get('resourcemap')
        DataStore._preloadkeys = config.get('preloadkeys')
        DataStore._preloadids = config.get('preloadids')
        DataStore._id_key_map = config.get('id_key_map')
        DataStore._preloadfile = config.get('preloadfile')
        DataStore._id_desc_map = config.get('id_desc_map')

    @staticmethod
    def loadcache():
        for key in DataStore._preloadkeys:
            try:
                DataStore.datadict[key] = pd.read_hdf(DATA_BASE_PATH+os.path.sep+DataStore._get_filename_by_key(key))
            except:
                logger.warning('key %s file can not load, maybe something wrong' % key)
        for id in DataStore._preloadids:
            key = DataStore._id_key_map.get(id)
            if key is None:
                raise CeQuantCoreError('error config preloadids')
            elif key not in DataStore._preloadkeys:
                try:
                    DataStore._datadict[key] = pd.read_hdf(DATA_BASE_PATH + os.path.sep + DataStore._get_filename_by_key(key))
                except:
                    logger.warning('key %s file can not load, maybe something wrong' % key)
        try:
            DataStore._cachedf = pd.read_hdf(DATA_BASE_PATH + os.path.sep + DataStore._preloadfile)
        except:
            logger.warnning('pre load file %s lost in %s' % (DataStore._preloadfile,DATA_BASE_PATH))

        DataStore._lastloadtime = datetime.now().strftime('%Y%m%d-%H%M%S')

    @staticmethod
    def _get_filename_by_key(key):
        keypath = key.split('.')
        filename = DataStore._resourcemap
        for n in keypath:
            filename = filename[n]
        return filename

    @staticmethod
    def get_resource_by_key(key):
        if key not in DataStore._datadict.keys():
            DataStore._datadict[key] = pd.read_hdf(DATA_BASE_PATH+os.path.sep+DataStore._get_filename_by_key(key))
            return DataStore._datadict[key]
        else:
            return DataStore._datadict[key]

    @staticmethod
    def get_resource_by_id(id):
        key=DataStore._id_key_map.get(id)
        if key is None:
            raise CeQuantInputError('input resource id is not exist')
        else:
            return DataStore.get_resource_by_key(key)

    @staticmethod
    def get_cache_status():
        return {'last load time':DataStore._lastloadtime,
                'last data time':DataStore._lastdatatime}

    @staticmethod
    def get_cache_by_ids(ids,addkeys=[]):
        try:
            colnames = [DataStore._id_key_map[id] for id in ids]
        except:
            raise CeQuantInputError('Input wrong id')
        if addkeys:
            colnames.extend(addkeys)
        return DataStore._cachedf[colnames]

    @staticmethod
    def get_desc_by_id(id):
        desc = DataStore._id_desc_map.get(id)
        if desc is None:
            logger.warning('can not find desc of %s',id)
        return desc

