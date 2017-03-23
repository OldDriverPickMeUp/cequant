#coding=utf-8

import os
from optparse import OptionParser
import importlib
import sys

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-m", "--model", action='store',type='string',dest="modelname",
                      help="find a model")
    parser.add_option("-b", "--basepath", action='store', type='string', dest="basepath",
                      help="set a basedir")
    parser.add_option("-s","--savepath",action='store',type='string',dest="savepath")

    (options, args) = parser.parse_args()
    if options.modelname is None:
        print 'Error must have a -m/--model option to set which model to load'
        exit(-1)
    if options.basepath is None:
        print 'Error must have a -b/--basepath option to set base import path'
        exit(-1)
    if options.savepath is None:
        print 'Error must have a -s/--savepath option to set csvfile savepath'
        exit(-1)

    #载入模块
    current_path=os.path.dirname(__file__)
    os.chdir(current_path)
    from worker import dumpworker
    os.chdir(options.basepath)
    sys.path.append(options.basepath)
    imported = importlib.import_module('dao.models.tablemodel')
    class_ = imported.__dict__.get(options.modelname)
    if class_ is None:
        print 'Error cannot find model class %s' % options.modelname

    dumpworker(class_(),options.savepath)
