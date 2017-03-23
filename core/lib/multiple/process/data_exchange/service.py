#coding=utf-8

class RequestService:
    """
        请求服务类，是用来相应进程中数据请求的类
    """
    def __init__(self,**para):
        """
            请求服务类构造函数
        :param para: datadict：数据字典
                    getfunc：获得数据的方法
        """
        self.datadict=para.get('datadict')
        self._getdataframe=para.get('getfunc',self._getinside)
        if self._getdataframe==self._getinside:
            if not self.datadict:
                raise Exception('You must init RequestService with a datadict or a getfunc')

    def _getinside(self,name):
        """
            默认获取数据的方法
        :param name: 数据名称
        :return: 数据
        """
        return self.datadict[name]

    def _handle_request(self,key,returnkey=None,constrain=None):
        """
            处理单个请求的函数
        :param key: 请求的键
        :param returnkey: 处理的别名
        :param constrain: 约束条件
        :return:
        """
        df=[]
        #print '_handle_request', key, returnkey,constrain
        def name_trans(key):
            tmp=[]
            for n in key:
                tmp.append(n.replace('.','_'))
            return tmp

        for item in key:
            df.append(self._getdataframe(item))
        if returnkey:
            realkey=returnkey
        else:
            realkey=name_trans(key)

        locald = {}
        cnt = 0
        for n in realkey:
            locald[n] = df[cnt]
            cnt += 1

        if constrain:
            exec(constrain.replace(' ','')) in None,locald
            todel=[]
            for n in locald:
                if n not in realkey:
                    todel.append(n)
            for n in todel:
                del locald[n]

        return locald,'-'.join(realkey)

    def handle_request(self,request):
        """
            处理全部请求
        :param request:请求对象
        :return:
        """
        cnt=0
        if type(request['key']) != list:
            key = [request['key']]
        else:
            key = request['key']

        if type(request['returnkey']) != list:
            returnkey = [request['returnkey']]
        else:
            returnkey = request['returnkey']

        if request.get('returnkey'):
            def get_returnkey(n):
                return returnkey[n]
        else:
            def get_returnkey(n):
                return None

        if type(request['constrain']) != list:
            constrain = [request['constrain']]
        else:
            constrain = request['constrain']

        if request.get('constrain'):
            def get_constrain(n):
                return constrain[n]
        else:
            def get_constrain(n):
                return None
        senddata={}

        for n in key:
            if type(n)!=list:
                tmpkey=[n]
            else:
                tmpkey=n
            returnkeyget=get_returnkey(cnt)
            if returnkeyget:
                if type(returnkeyget) != list:
                    tmpreturnkey = [returnkeyget]
                else:
                    tmpreturnkey=returnkeyget
            else:
                tmpreturnkey = returnkeyget
            data,name=self._handle_request(tmpkey,tmpreturnkey,get_constrain(cnt))
            senddata[name]=data
            cnt+=1
        return {'head':request.get('head'),
                'data':senddata}