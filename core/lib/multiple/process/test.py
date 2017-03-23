#coding=utf-8
import time
def inner_print(x):
    print x


def inner_stop(x):
    return -1

default_handler={ 'print': inner_print,
                   'stop': inner_stop}

"""
def testwork(index):
    print 'in testwork'
    #init DataAcquire
    acquire=DataAcquire()
    #init data server in local
    #init local data
    data = {}
    data['col1'] = [1, 2, 3, 4, 5]
    data['col2'] = [1, 2., 3, 5, 7.]
    data['col3'] = ['x', 'v', 'c', 'a', 1]
    df = pd.DataFrame(data)
    df.set_index(['col1'], inplace=True)

    data = {}
    data['ind'] = [7, 9, 20]
    data['col2'] = [1.01, 2.1, 34]
    data['col3'] = ['abc', 'edf', 808.7]
    df2 = pd.DataFrame(data)
    df2.set_index(['ind'], inplace=True)

    datadict = {'test.data': df,
                'test.data2': df2}
    server = RequestService(datadict=datadict)


    #another way to init local data
    #hdfpath is data's local path
    hdfpath='local path'
    #df_name_file is data filenames' local path
    import json
    df_name_file='local df_names file name'
    with open(df_name_file) as f:
        df_names=json.load(f)
    def getdataframe(key):
        path = key.split('.')
        if len(path) != 2:
            raise Exception('Error in geting DataFrames:key struct is not right')
        basicpath = '' if hdfpath == '' else hdfpath + os.path.sep
        return pd.read_hdf(basicpath + df_names[path[0]][path[1]])

    server = RequestService(getfunc=getdataframe)


    #key=['testdata','testdata2']
    key = [['test.data', 'test.data2']]
    #returnkey=['dfs','df2']
    #returnkey = [['dfs', 'df2']]
    #returnkey=None
    #constrain=['dfs=dfs.ix[3:5]','df2=df2.ix[7:11]']
    #constrain = ['dfs=dfs.ix[3:5]\ndf2=df2.ix[7:11]']
    constrain = ['test_data=test_data.ix[3:5]\ntest_data2=test_data2.ix[7:11]']
    def  wrapper1(**para):
        return server.handle_request(acquire.getdata_local(key=para['key'], constrain=para.get('constrain'),returnkey=get('returnkey')))
    def  wrapper2(**para):
        return acquire.getdata(key=para['key'], constrain=para.get('constrain'),returnkey=para.get('returnkey'))
    get_data=wrapper1


    while True:
        time.sleep(10)
        print 'request....'
        data = get_data(key=key, constrain=constrain)
        #another get data method
        data = server.handle_request(acquire.getdata_local(key=key, constrain=constrain,returnkey=returnkey))

        print 'in process\n\thead\n',data['head'],'\n\tbody\n',data['data']
        time.sleep(3)
        break
        if data==-1:
            print 'data is',data
            break
    print 'in process',index,'end'
"""


def wrapper(para, **kwargs):
    acquire = kwargs.get('acquire')
    print 'in process'
    para['func'](para['in'], acquire)


def testworker(inp, **para):
    print inp, 'anumber'
    # import time
    time.sleep(5)
    print 'before return'
    return inp* 892


"""
if __name__=='__main__':
    #key1=['1','2',['4','5'],'sad','asd',['123']]
    #key2='1'
    #key3=['1','2','3']
    #key=key3
    #a=RequestExchange(key=key)
    #print a.test(key1)

    import pandas as pd
    data={}
    data['col1']=[1,2,3,4,5]
    data['col2']=[1,2.,3,5,7.]
    data['col3']=['x','v','c','a',1]
    df=pd.DataFrame(data)
    df.set_index(['col1'],inplace=True)

    data = {}
    data['ind'] = [7,9,20]
    data['col2'] = [1.01, 2.1, 34]
    data['col3'] = ['abc', 'edf', 808.7]
    df2 = pd.DataFrame(data)
    df2.set_index(['ind'], inplace=True)

    datadict={'test.data':df,
              'test.data2':df2}

    serve=RequestService(datadict=datadict)
    p=MyPoolwithPipe(1)
    #print 'after'
    #inpara={'func':testwork,'in':1}
    p.apply_async(wrapper,(inpara,))
    #print re.get()
    time.sleep(1)
    #p.set_stop()
    req=p.get_data()
    print 'in father req',req
    if req==-1:exit()
    p.send_data(serve.handle_request(req))
    time.sleep(5)
    #print req
    #import time
    #time.sleep(1)
    #print p.get_data()
    #p.send_data('print',123)
    #time.sleep(1)
    #print p.get_data()
    #p.send_data('print',df)
    #time.sleep(1)
    #time.sleep(1)
    #p.send_data('stop')
    #time.sleep(1)
    #re=p.apply_async(testworker,(2,))
    #time.sleep(3)
    #print re.get()
    #p.apply_async(testworker,(2,))
    print 'father end'
"""
