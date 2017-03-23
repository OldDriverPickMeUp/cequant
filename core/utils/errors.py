#coding=utf-8

import sys
import traceback

class CeQuantError(Exception):

    def __init__(self, detail, trace=False,full=False):
        if trace:
            self.err_source = self.get_err_source(full)
        else:
            self.err_source = {}
        self.detail = detail
        self.message = detail

    @staticmethod
    def get_error_info(full):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tracelist=traceback.extract_stack(exc_traceback)
        if full:
            return tracelist
        else:
            return traceback.extract_tb(exc_traceback)[-1]

    @staticmethod
    def get_format_error_info():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        errfile,errline,errmodule,errloc = traceback.extract_tb(exc_traceback)[-1]
        #return {'file':errfile,
        #            'line':errline,
        #            'module':errmodule,
        #            'loc':errloc}
        return 'Catched error in %s  line %s  in %s-%s' % (errfile,errline,errmodule,errloc)
    @classmethod
    def get_err_source(cls,full):
        return cls.get_format_error_info()


class CeQuantCoreError(CeQuantError):
    pass

class CeQuantConfigError(CeQuantCoreError):
    pass

class CeQuantUserError(CeQuantError):
    pass

class CeQuantInputError(CeQuantUserError):
    pass

class CeQuantTaskError(CeQuantUserError):
    pass

class CeQuantDBError(CeQuantError):
    pass
