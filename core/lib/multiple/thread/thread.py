#coding=utf-8

import threading

class MyThread(threading.Thread):

    def __init__(self,**para):

        threading.Thread.__init__(self)
        self.func=para.get('func',None)
        if not self.func:
            raise Exception('MyThread Object must have a function to run')
        self.args=para.get('args',None)

    def run(self):

        self.result=self.func(self.args)

    def getresult(self):

        return self.result