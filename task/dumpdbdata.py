#coding=utf-8

from core.scanner import set_instruct
from core.taskhandler.task import InstrcutInfo,TraceMaker,TaskInfo

@set_instruct('dumpdbdata')
def dumpdbdata():
    instruct = InstrcutInfo('dumpdbdata')               # dumpdbdata只是指令显示的名字，并不是指令的命令名，可以写成unicode的中文

    trace = TraceMaker().add_node('dumpdata.stock_value_factor').get_trace()
    subtask = TaskInfo('stock_value_factor').set_trace(trace)
    instruct.add_task(subtask)

    trace = TraceMaker().add_node('dumpdata.stock_report_factor').get_trace()
    subtask = TaskInfo('stock_report_factor').set_trace(trace)
    instruct.add_task(subtask)

    return instruct



