#coding=utf-8

import subprocess
import platform
import os

from core.utils.errors import CeQuantCoreError,CeQuantTaskError

def dump_trace(modelname,savepath):

    basepath = os.getcwd()
    filenamepath = os.path.dirname(__file__)
    filename = os.path.sep.join([filenamepath,'dumpdbdata.py'])
    if not os.path.exists(filename):
        raise CeQuantTaskError('Cannot find dumpdata.py file in path %s' % filenamepath)

    #检查平台
    if platform.system()=='Windows':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
        try:
            p = subprocess.Popen(['pypy', filename,'-m',modelname,'-b',basepath,'-s',savepath], startupinfo=si, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        except WindowsError:
            raise CeQuantCoreError('current operating system do not have pypy')
    elif platform.system() == 'Linux':
        try:
            p = subprocess.Popen(['pypy', filename,'-m',modelname,'-b',basepath,'-s',savepath], stdout=subprocess.PIPE,stdin=subprocess.PIPE,\
                                 stderr=subprocess.PIPE)
        except OSError:
            raise CeQuantCoreError('current operating system do not have pypy')

    else:
        raise CeQuantCoreError('current operating system is neither Windows nor Linux')

    p.wait()
    out = p.stdout.read()
    errout = p.stderr.read()
    desc = 'stdout:\n %s stderr:\n %s' % (out,errout)
    return_code = p.returncode
    if return_code != 0:
        raise CeQuantTaskError(desc)
    return True


