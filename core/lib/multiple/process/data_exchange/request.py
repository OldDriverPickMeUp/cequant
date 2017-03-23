#coding=utf-8

class RequestExchange:
    """
    request exchange object is used to gennerate request infomation which will be send to its father process
    request at most 4 parameters:
        head:   optional,
                head of this request as a tag to recognise
        key:    essential,
                key is the unique name of data in father process
                key can be:
                    a name,eg. equ_factor_AF
                    list of names,eg. [equ_factor_AF.name1,equ_factor_BF.name2]
                    several lists of names,eg. [[equ_factor_AF.name1,equ_factor_BF.name2],[equ_factor_AF.name3]] or
                                                [[equ_factor_AF.name1,equ_factor_BF.name2],equ_factor_AF.name3]
                request for each sub-list of keynames
                a DataFrame of several columns match keynames will be returned
        constrint:  optional,
                    constrint like where clauses in sqls
                    constrint can be:
                    a constrint object,eg. constrint1
                    list of constrint objects,eg. [constrint1,constrint2]
        returnkey:  optional,
                    returnkey is the keyname in recived data dict
                    returnkey can be:
                    a returnkey object,eg. returnkey1
                    several returnkeys,eg. [returnkey1,returnkey2,returnkey3]
    """
    def __init__(self,**para):
        """
            请求数据的对象
        :param para: head:数据头
                    key:请求的键
                    constrain:约束条件
                    returnkey:返回别名
        """
        self.head=para.get('head')
        self.key=para['key']
        self.constrint=para.get('constrain')
        self.returnkey=para.get('returnkey')
        self._check()

    def _check(self):
        """
            检查格式合法性
        :return:
        """
        codekey=self._encode(self.key)
        if self.constrint:
            codecon=self._encode(self.constrint)
            if len(codekey)!=len(codecon):
                raise Exception('constrint and key do not match')
        if self.returnkey:
            coderet=self._encode(self.returnkey)
            if coderet!=codekey:
                raise Exception('returnkey and key do not match')

    def _encode(self,obj):
        """
            对数据格式进行编码
        :param obj: 单个数据对象
        :return: 返回结构编码
        """
        def haslist(obj):
            tpobj = type(obj)
            if tpobj != list and tpobj != tuple:
                return '1'
            else:
                for n in obj:
                    tpobj = type(n)
                    if tpobj==list and tpobj==tuple:
                        raise Exception('parameter too deep')
                return str(len(obj))
        tpobj=type(obj)
        if tpobj!=list and tpobj!=tuple:
            return '1'
        else:
            code=''
            for n in obj:
                code+=haslist(n)
            return code

    def __call__(self):
        """
            请求数据对象的__call__方法
        :return:
        """
        return {'head':self.head,
                'key':self.key,
                'constrain':self.constrint,
                'returnkey':self.returnkey}
