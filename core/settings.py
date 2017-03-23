#coding=utf-8


#核心一些参数
INSTRUCT_MAX_ITEMS_PAGE = 100
MAX_PARALLEL_PROCESS = 5            #进程池进程数


#数据路径配置 不带最后一个分隔符
DATA_BASE_PATH = '/root/CeQuantPlatinumData'

#扫描trace所在的目录，相对于根目录
TRACE_SERVICE_PATH = 'service'

#扫描instruct/task所在的目录，相对于根目录
INSTRUCT_TASK_PATH = 'task'

#Port
SOCKET_PORT = 7995
WEB_PORT = 8999

#socket
SOCKET_EOF = '\r\n\r\n'
SOCKET_TIMEOUT = 120       #2分钟超时

# 数据库
# 线下同步后数据库
DB_OFFLINE_STOCK = {'host':'192.168.1.205',
'port':3308,
'user':'stock',
'passwd':'stock123456',
'db':'stock'}
# 线下财汇原始数据库
DB_OFFLINE_ORG_STOCK = {'host':'192.168.1.205',
'port':3307,
'user':'stockdata',
'passwd':'stockdata123456',
'db':'stockdata'}
# 线下同步线上数据库
DB_OFFLINE_SYN_ONLINE = {'host':'192.168.1.204',
'port':3340,
'user':'uat',
'passwd':'root123456',
'db':'peon'}
# 平台保存报告、索引及相关信息的数据库
DB_PLATFORM_DATA = {
    'host': '192.168.1.114',
    'port': 3506,
    'user': 'myuser',
    'passwd': '37m6nef',
    'db': 'backtestdata'
}
