#encoding=utf-8
import json
#import sys
import numpy as np
import re
import socket
import time

class ShellClient:
    def __init__(self, head='deb', **kwargs):
        self._head = head
        self.addr = kwargs.get('addr')
        # self.namepatten
        self._vardict = {}
        self._cmddict = {}
        self._loadcmddict()
        self._loadvardict()
        self._curloaded = 0
        self._helptext = 'show command to lookup all command\nshow variable to show all variables'
    def _checkname(self,strings):
        p='\D*'
        for string in strings:
            obj=re.match(p,string)
            if obj.group(0)=='':
                raise Exception('wrong naming')
            #if string.find('')

        if self._hasobj('.'.join(strings))!=None:
            raise Exception('name already used')
    def _createnewvar(self,para):
        #print para
        paras=para.split(' ')
        for p in paras:
            p=p.strip()
        name=paras[0]
        value=paras[1] if len(paras)==2 else None
        #print name
        namepath=name.split('.')
        #print 'after'
        self._checkname(namepath)
        def create(pathlist,dd):
            if len(pathlist)==1:
                dd[pathlist[0]]=np.NAN
            else:
                if dd.get(pathlist[0])==None:
                    dd[pathlist[0]]={}
                create(pathlist[1:],dd[pathlist[0]])
        #print 'vv'
        create(namepath, self._vardict)
        if value==None:
            return
        obj=self._hasobj(value)
        if obj==None:
            obj=json.loads(value)
        #print 'vv'
        self._setvar(name,obj)

    def _del(self,string):
        strings=[n.strip() for n in string.split(' ')]
        for n in strings:
            if self._hasobj(n)==None:
                raise Exception('没有要删除的变量:'+n)
        for n in strings:
            self._delvar(n)

    def _delvar(self,path):
        pathlist = path.split('.')
        n = len(pathlist)
        if n == 1:
            del self._vardict[pathlist[0]]
        elif n == 2:
            del self._vardict[pathlist[0]][pathlist[1]]
        elif n == 3:
            del self._vardict[pathlist[0]][pathlist[1]][pathlist[3]]
        elif n == 4:
            del self._vardict[pathlist[0]][pathlist[1]][pathlist[3]][pathlist[4]]

    def _load(self, para):
        with open(para) as f:
            loadobj=json.load(f)
        self._curloaded+=1
        self._vardict['load-'+str(self._curloaded)]=loadobj
        return '你的文件已经被载入到load-'+str(self._curloaded)

    def _loadcmddict(self, path=None):
        self._cmddict['print']=lambda x:str(self._getobj(x))
        self._cmddict['create']=self._createnewvar
        #self._cmddict['=']='like ='
        self._cmddict['quit']=lambda x=-1:x
        self._cmddict['help']=lambda x=None:self._helptext
        self._cmddict['show']=self._show
        self._cmddict['send']=self._sendmsg
        self._cmddict['save']=self._save
        self._cmddict['load']=self._load
        self._cmddict['del']=self._del

    def _loadvardict(self,path=None):
        self._vardict['version']='v0.1'
        self._vardict['config']={'stock_count':5,'commission_ratio':0.0003,\
                'slipping_ratio':0.00246,'initial_nav':1000000.0,\
                'stamp_ratio':0.001,'start_date':"20160101",\
                'end_date':"20160629",'factorid':[30,55,49]}
        if self.addr:
            self._vardict['conn'] = {'host': self.addr[0], 'port': self.addr[1]}
        else:
            self._vardict['conn'] = {'host': '192.168.1.114', 'port': 3508}
        self._vardict['stop']={'funcname':'stoppool','taskname':'stoppool'}
        self._vardict['check']={'funcname':'check','taskname':'check'}
        self._vardict['empty']={'funcname':'emptytrash','taskname':'emptytrash'}
        self._vardict['kill']={'funcname':'kill','taskname':'kill'}
        self._vardict['instruct']={'funcname':'showinstruct','taskname':'showinstruct'}
        self._vardict['allins'] = {'funcname': 'showallinstruct', 'taskname': 'showallinstruct'}
        self._vardict['reload']={'taskname':'reload_data_cache'}
        self._vardict['show_data_status']={'taskname':'show_data_status'}
        self._vardict['backtest_cfg_base']={'factor':None,
                                       'timming':None,
                                       'start':None,
                                       'end':None,
                                       'dir':None,
                                       'weight':None}
        self._vardict['backtest_cfg_template']={'factor':None,
                                       'timming':None,
                                       'start':None,
                                       'end':None,
                                       'dir':None,
                                        'id':None,
                                            'name':None,
                                            'author':None,
                                            'commissionRatio':0.0003,
                                            'stampRatio':0.001,
                                            'slippage':0.00246,
                                            'initialCash':1000000.0}

        self._vardict['start_auto_empty']={'funcname':'start_auto_empty','taskname':'start_auto_empty'}
        self._vardict['end_auto_empty'] = {'funcname': 'end_auto_empty', 'taskname': 'end_auto_empty'}
        self._vardict['benchmark']={'taskname':'backtest',
                                    'receipt':12312312,
                                    'cfg':{'factor':[200,201,202,203,204,
                                                        100,101,102,
                                                        500,502,503,
                                                        600,601,602,603,604,605,
                                                        400,401,402,403],
                                            'timming':[5001],
                                           'receipt':12312817928127,
                                            'start':'20150101',
                                            'end':'20160101',
                                           'author': 'Admin',
                                           'name': 'Benchmark',
                                            }
                                    }
        self._vardict['new_backtest']={'trace':{'trace':['backtest','calc_index',['to_db','to_excel'],'to_ftp'],
                                                  'pre_thread':'getdata_for_backtest'},
                                       'taskname':'backtest',
                                       'cfg': {'factor': [200, 201, 202, 203, 204,
                                                          100, 101, 102,
                                                          500, 502, 503,
                                                          600, 601, 602, 603, 604, 605,
                                                          400, 401, 402, 403],
                                               'timming': [5001],
                                               'start': '20150101',
                                               'end': '20160101',
                                               'author': 'new_backtest',
                                               'name': 'Benchmark',
                                               }
                                       }
        self._vardict['factorprepare1'] = {'taskname': 'factorprepare', 'subid': 0}
        self._vardict['factorprepare2'] = {'taskname': 'factorprepare', 'subid': [1, 2, 3, 4, 5, 6]}
        self._vardict['factorrun'] = {'taskname': 'factorrun', 'subid': 'all'}
        self._vardict['technitalrun'] = {'taskname': 'technitalrun', 'subid': 'all'}
        self._vardict['backtestdataprepare'] = {'taskname': 'backtestdataprepare', 'subid': 'all'}
        self._vardict['merge_rating'] = {'taskname': 'merge_rating'}
        self._vardict['terminate']={'taskname':'terminate'}
        self._vardict['show_variables']={'taskname':'show_variables'}
        self._vardict['opt_index'] = {'taskname': 'opt_index',
                                      'opt_index':5001,
                                      'opt_param':'10,1.5,1.5',
                                      'cfg': {'factor': [200, 201, 202, 203, 204,
                                                         100, 101, 102,
                                                         500, 502, 503,
                                                         600, 601, 602, 603, 604, 605,
                                                         400, 401, 402, 403],
                                              'timming': [5001],#Boll
                                              'receipt': 12312817928127,
                                              'start': '20150101',
                                              'end': '20160101',
                                              'author': 'optimizer',
                                              'name': 'opt_test',
                                              }
                                      }
        self._vardict['opt_index_all'] = {'taskname': 'opt_index_all',
                                      'opt_index': 5001,
                                      'opt_param': '10,1.5,1.5',
                                      'cfg': {'timming': [5001],  # Boll
                                              'start': '20150101',
                                              'end': '20160101',
                                              'author': 'optimizer',
                                              'name': 'opt_test',
                                              'strategyClassKey':'astockTimmingStrategy',
                                              'symbol':['2070000060']
                                              }
                                      }
        self._vardict['backtest_tdx']={'taskname':'backtest_tdx',
                                       'yourcode':'huangjinshouzhi',
                                       'which': 'huangjinshouzhi',
                                       'opt_param': '10',
                                       'cfg':{'start':'20080101',
                                              'end':'20161120',
                                              'author':'wangby',
                                              'name':'tdx_transform',
                                              'strategyClassKey': 'astockTimmingStrategy',
                                              'otherSpecialParamDict':{'indexFlag':True,},
                                              'symbol': ['2070000060'],
                                              'factor':[],
                                              'timming':[],
                                              }
                                       }
        self._vardict['backtest_tdx_stock'] = {'taskname': 'backtest_tdx',
                                         'yourcode': 'huangjinshouzhi',
                                         'which': 'huangjinshouzhi',
                                         'opt_param': '10',
                                         'cfg': {'start': '20080101',
                                                 'end': '20161120',
                                                 'author': 'wangby',
                                                 'name': 'tdx_transform',
                                                 'strategyClassKey': 'aStockTimming',
                                                 'otherSpecialParamDict': {'indexFlag': False,},
                                                 'symbol': ['2070000060'],
                                                 'factor': [],
                                                 'timming': [],
                                                 }
                                         }
        self._vardict['corr_factor'] = {'taskname': 'correlate_factor',
                                      'cfg': {'factor': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,
                                                         100, 101, 102,
                                                         200,201,202,203,204,
                                                         300,301,302,303,304,305,
                                                         400, 401, 402, 403,
                                                         500, 502, 503,
                                                         600, 601, 602, 603, 604, 605
                                                         ],
                                              'timming': [5008],  # Boll
                                              'start': '20150101',
                                              'end': '20160101',
                                              'author': 'correlater',
                                              'name': 'correlate_test'
                                              },
                                        'real_name':1,
                                        'save_hdf':0
                                      }

    def _save(self,para):
        if para.find(' ')==-1:
            #只有一个参数
            dest=para
            obj=self._vardict
        else:
            paralist=[n.strip() for n in para.split(' ')]
            if len(paralist)>2:raise Exception('不能识别的参数')
            objname=para[0]
            dest=para[1]
            obj=self._hasobj(objname)
            if obj==None:raise Exception('找不到可以保存的'+objname)
        with open(dest,'w') as f:
            json.dump(obj,f)
        return '数据已经储存在文件：'+dest

    def start(self):
        while True:
            cmdstr=raw_input(self._head+'>')
            cmdstr=cmdstr.replace("'",'"')
            #print cmdstr
            answer=self._switchstring(cmdstr)
            #print answer
            if answer!=None and type(answer) == str:
                print str(answer)
            elif answer==-1:
                break

    def command(self,cmdstr):
        cmdstr = cmdstr.replace("'", '"')
        # print cmdstr
        answer = self._switchstring(cmdstr)
        return answer

    def _show(self,para=None):
        #print para
        if para in ['command','cmd','commands']:
            return str(self._cmddict.keys())
        elif para in ['variable','var','variables']:
            return str(self._vardict.keys())
        elif para==None:
            return 'cmds:'+str(self._cmddict.keys())+'\nvars:'+str(self._vardict.keys())
            #return self._helptext
        else:
            return str(self._getobj(para).keys())

    def _sendmsg(self,string):
        obj=self._getobj(string)
        #增加时间戳
        obj['receipt']=int(time.time()*100)
        sendstr = json.dumps(obj)+'\r\n\r\n'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(25)
        addr=(self._vardict['conn']['host'],self._vardict['conn']['port'])
        try:
            sock.connect(addr)
            print addr, 'connected'
        except:
            print 'error in connecting', addr
            return False
        sock.send(sendstr)
        try:
            answer = sock.recv(1024)
            cnt = 0
            while True:
                sock.setblocking(1)
                cnt += 1
                try:
                    tmp = sock.recv(1024)
                    if tmp == '':
                        break
                except:
                    break
                if cnt > 200: break
                answer += tmp
        except:
            answer = 'timout error'
        # self.sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        #print answer
        return answer

    def sendmsg(self, obj,receipt=None):
        #obj = self._getobj(string)
        if not receipt:
            obj['receipt']=int(time.time()*100)
        else:
            obj['receipt']=receipt
        sendstr = json.dumps(obj)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(25)
        addr = (self._vardict['conn']['host'], self._vardict['conn']['port'])
        try:
            sock.connect(addr)
            print addr, 'connected'
        except:
            print 'error in connecting', addr
            return False
        sock.send(sendstr)
        try:
            answer = sock.recv(1024)
            cnt=0
            while True:
                sock.setblocking(1)
                cnt+=1
                try:
                    tmp = sock.recv(1024)
                    if tmp=='':
                        break
                except:
                    break
                if cnt>200:break
                answer += tmp
        except:
            answer = 'timout error'
        # self.sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        # print answer
        return answer

    def _switchstring(self,string):
        if string.find('=')!=-1:
            strings=string.split('=')
            #print strings
            if len(strings)>2:
                return 'error in ='
            for n in strings:
                n=n.strip()
            try:
                #print n[1]
                obj=self._hasobj(strings[1])
                #print obj,strings[1]
                if obj!=None:
                    self._setvar(strings[0],obj)
                else:
                    value=json.loads(strings[1])
                    self._setvar(strings[0],value)
            except Exception as e:
                return e.message
            #self._getobj(n[0])=value
        else:
            return self._answercmd(string)
    def _answercmd(self,string):
        nstr=string.strip()
        hasobj=self._hasobj(nstr)
        #print nstr,hasobj
        #print nstr,self._cmddict.keys()
        if nstr in self._cmddict.keys():
            return self._cmddict[nstr]()
        elif hasobj!=None:
            return str(hasobj)
        else:
            loc=nstr.find(' ')
            if loc==-1:return '没有这个变量'
            cmd=nstr[:loc]
            para=nstr[loc+1:].strip()
            #print cmd,para
            return self._execcmd(cmd,para)

    def _setvar(self,path,value):
        pathlist = path.split('.')
        n=len(pathlist)
        if self._hasobj(path)==None:
            self._createnewvar(path)
            print '新变量被创建:'+path
        if n==1:self._vardict[pathlist[0]]=value
        elif n==2:self._vardict[pathlist[0]][pathlist[1]]=value
        elif n==3:self._vardict[pathlist[0]][pathlist[1]][pathlist[3]]=value
        elif n==4:self._vardict[pathlist[0]][pathlist[1]][pathlist[3]][pathlist[4]]=value
        else:
            raise Exception('Not Support now')
    def _getobj(self,string):
        path=string.split('.')
        #print path
        def getkey(pathlist,dd):
            #print dd,pathlist
            if len(pathlist)==1:
                #print dd,'asdp'
                #print dd[pathlist[0]]
                return dd[pathlist[0]]
            else:
                #print dd[pathlist[0]]
                return getkey(pathlist[1:],dd[pathlist[0]])
        return getkey(path,self._vardict)

    def _hasobj(self,string):
        try:
            return self._getobj(string)
        except:
            return None

    def _execcmd(self,cmd,para):
        try:
            #print para
            return self._cmddict[cmd](para)
        except Exception as e:
            #raise e
            return 'Error:'+e.message
            #print sys.exc_info()
            #return str(sys.exc_info())
        
if __name__=='__main__':
    sc=ShellClient()
    #sc.sendmsg()
    sc.start()
