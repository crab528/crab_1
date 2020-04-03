import os
import datetime

def filePath(fileDir='data',fileName='login.yaml'):
    '''
    :param fileDir 文件目录
    :param fileName 文件名称
    '''
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),fileDir,fileName
    )

def writeContent(content):
    # print('writeTime:',datetime.datetime.now())
    with open(filePath(fileName='bookID'),'w')as f:
        f.write(str(content))

def readContent():
    # print('readTime:',datetime.datetime.now())
    with open(filePath(fileName='bookID'),'r')as f:
        return f.read()
