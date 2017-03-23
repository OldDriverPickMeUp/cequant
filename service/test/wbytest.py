#coding=utf-8

import time

from core.scanner import set_trace,set_instruct
from core.taskhandler.task import InstrcutInfo,TraceMaker,TaskInfo


# service 编写样例
@set_trace('testnode1')         #set_trace 注册一个trace的节点的服务
def testnode1(iostream,cmd):
    #输入参数必须是iostream和cmd
    #iostream是输入数据流，以这样的方式保存数，所有数据从中获得
    #cmd为输入的控制字，控制的参数，所有配置参数从中获得

    #用户程序段
    time.sleep(10)
    #用户程序段

    #必须以数据流作为唯一的输出量
    return iostream

@set_trace('testnode2')
def testnode2(iostream,cmd):
    print 'now in testnode2'
    time.sleep(2)
    raise Exception('mmmmm')
    return iostream


#指令是一个任务集，里面包含1个或者多个任务
@set_instruct('testinstruct1')  #set_instruct 注册一个instruct指令
def bulidintest():                  #这个函数为一个指令的生成函数
    trace=TraceMaker().add_node('testnode1').get_trace()    #tracemaker帮助生成一个trace

    #必须返回一个InstructInfo
    #返回的这个Instruct会被扫描并生成相应的InstructInfo信息
    #当一个指令缺省内部任务时
    #会自动填充一个任务，作为唯一的任务
    return InstrcutInfo(name='wbytest').set_trace(trace)

#一个有两个子任务的例子
@set_instruct('testinstruct2')          #注册一个instruct指令
def buildintest2():
    trace = TraceMaker().add_node('testnode1').add_node('testnode2').get_trace()    #创建一个公用的trace
    instruct = InstrcutInfo('wbytest').set_trace(trace)      #生成一个指令并设置它的执行方法

    subtask =  TaskInfo('testsubtask1')         #生成一个子任务
    instruct.add_task(subtask)         #将子任务挂载到指令

    subtask = TaskInfo('testsubtask2')      #生成第二个子任务
    subtrace = TraceMaker().add_node('testnode2').get_trace()   #为第二个子任务生成一个trace
    subtask.set_trace(subtrace)         #为第二个子任务设置不同的trace 执行方式
                                        #当子任务没有设置执行方式时
                                        #执行时会调用父指令的执行方式 trace
    instruct.add_task(subtask)          #挂载第二个子任务

    #生成了一个新的指令
    #必须要通过返回的方式来注册
    return instruct