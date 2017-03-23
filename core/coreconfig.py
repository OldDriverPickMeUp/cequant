#coding=utf-8

from .utils.errors import CeQuantConfigError,CeQuantUserError

class ConfigManager:
    def __init__(self):
        self._dict = {}
        self.lock = False

    def set(self, key, obj):
        if self.lock:
            raise CeQuantUserError('config object locked')
        if key in self._dict:
            raise CeQuantConfigError('key %s allready exists' % key)
        self._dict[key] = obj
        return self

    def get(self, key):
        obj = self._dict.get(key)
        if obj is None:
            raise CeQuantConfigError('key %s does not exists' % key)
        if isinstance(obj,ConfigManager):
            obj.lock = self.lock
        return obj

class GlobalConfig:
    _config = None

    @staticmethod
    def initialize(config):
        if not isinstance(config,ConfigManager):
            raise CeQuantConfigError('config object must be instance of ConfigManager')
        GlobalConfig._config = config
        GlobalConfig._config.lock = True

    @staticmethod
    def get_config(self,key):
        pass
