#coding=utf-8
from core.scanner import set_trace


# 这里是写必须实现的内置trace

@set_trace('bypass')
def bypass(x,y):
    return x
