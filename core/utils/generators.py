#coding=utf-8

def IdGenerator():
    index = 1
    while True:
        yield index
        index += 1

