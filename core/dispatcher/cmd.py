#coding=utf-8

from ..utils.errors import CeQuantInputError

class CommandManager:
    def __init__(self, dispatcher):
        self.dispatcher=dispatcher

    def initialize(self):

        instructmanager = self.dispatcher.instructmanager
        taskmanager = self.dispatcher.taskmanager
        tmp = {}

        # 按页显示目前所有的instruct
        # 以页数0开始，增加，0显示最新的instruct
        # 每页显示固定个
        # 如果超过最大页数会返回空
        def check(kwargs):
            page = kwargs.get('page')
            if page is None:
                page = 0
            return instructmanager.get_instruct(page)
        tmp['check'] = check

        # 清除已经正确执行完毕的instruct
        # 会保留错误的以及未完成的instruct
        def clean(kwargs):
            return instructmanager.clean_instruct()
        tmp['clean'] = clean

        # 指定instruct id 的 全部子任务
        # 当instruct出错时，可以使用它返回所有instruct下的子任务
        # 在子任务中可以找到是哪个任务出错了
        # 当返回的子任务出错时
        # 会返回栈追踪的信息
        def get_subtask(kwargs):
            instruct_id = kwargs.get('instruct_id')
            if instruct_id is None:
                raise CeQuantInputError('get_subtask command input dick should have a key named instruct_id')
            try:
                instruct_id = int(instruct_id)
            except:
                raise CeQuantInputError('instruct_id should be type of int or can be transformed into type int')
            return instructmanager.get_subtask(instruct_id)
        tmp['get_subtask'] = get_subtask

        # 重新载入所有的模块
        # 会先删除以前所有的trace，instruct
        # 然后重新扫描模块
        # 如果有新模块将会被扫描进入
        # 应在调试时使用
        # 当在执行任务时执行不确定会发生什么事情
        def rescan(kwargs):
            from ..settings import TRACE_SERVICE_PATH,INSTRUCT_TASK_PATH
            from ..scanner import Scanner
            Scanner.clear()
            Scanner.scan_path(TRACE_SERVICE_PATH)
            Scanner.scan_path(INSTRUCT_TASK_PATH)
            return {'result':'trace and instruct loaded'}
        tmp['rescan'] = rescan


        self.cmd_list = tmp

    def excute(self,cmd,kwargs):
        return self.cmd_list[cmd](kwargs)

    def hascmd(self,cmdname):
        if cmdname in self.cmd_list:
            return True
        else:
            return False



