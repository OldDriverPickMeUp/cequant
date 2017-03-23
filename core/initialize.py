#coding=utf-8

from .coreconfig import ConfigManager

def get_global_config(scanner):

    leadcfg = ConfigManager()

    cfgobj = ConfigManager().set('tracemanager',scanner.trace_store)      #最大并行任务、tracemanager

    leadcfg.set('taskmanager',cfgobj)

    cfgobj = ConfigManager().set('instruct_info',scanner.instruct_store)    #设置指令信息

    leadcfg.set('instructmanager',cfgobj)

    return leadcfg
