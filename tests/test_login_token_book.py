from base.method import Requests
from utils.operationExcel import OperationExcel,excelValues
from common.public import *
import pytest
import json
import allure

excel=OperationExcel()
obj=Requests()

@pytest.mark.parametrize('datas',excel.runs())
def test_login_book(datas):
    '''对请求参数进行反序列化处理'''
    params = datas[excelValues.params]
    if len(str(params).strip()) == 0:
        pass
    elif len(str(params).strip()) > 0:
        params = json.loads(params)
        # print(params)
    '''对请求头进行反序列化处理'''
    headers = datas[excelValues.headers]
    if len(str(headers).strip()) == 0:
        pass
    elif len(str(headers).strip()) > 0:
        headers = json.loads(headers)
        # print(headers)

    #执行前置条件关联的测试点
    r=obj.post(
        url=excel.case_prev(datas[excelValues.casePre])[excelValues.caseUrl],
        json=json.loads(excel.case_prev(datas[excelValues.casePre])[excelValues.params]))
    #获取结果信息
    prevResult=r.json()['access_token']
    #替换被关联测试点中请求头信息的变量
    headersG=excel.prevHeaders(prevResult)


    def verify(r):
        assert datas[excelValues.expect] in json.dumps(r.json(), ensure_ascii=False)
        assert r.status_code==datas[excelValues.statusCode]

    def setUrl():
        url = str(datas[excelValues.caseUrl]).replace('{bookID}', readContent())
        return url

    if datas[excelValues.method]=='get':
        if '/v1/api/books'in datas[excelValues.caseUrl]:
            r = obj.get(url=datas[excelValues.caseUrl], headers=headersG)
            verify(r)
        else:
            r = obj.get(url=setUrl(), json=params, headers=headersG)
            verify(r)
    elif datas[excelValues.method]=='post':
        r=obj.post(url=datas[excelValues.caseUrl],json=params,headers=headersG)
        writeContent(content=str(r.json()[0]['datas']['id']))
        verify(r)
    elif datas[excelValues.method]=='put':
        r = obj.put(url=setUrl(), json=params,headers=headersG)
        verify(r)
    elif datas[excelValues.method]=='delete':
        # r = obj.delete(url=datas[excelValues.caseUrl], headers=headersG)
        r=obj.delete(url=setUrl(),headers=headersG)
        verify(r)

# if __name__=='__main__':
#     pytest.main(["-s", "-v", "test_login_token_book.py", "--alluredir", "./report/result"])
#     import subprocess
#     subprocess.call('allure generate report/result/ -o report/html --clean', shell=True)
#     subprocess.call('allure open -h 127.0.0.1 -p  8088 ./report/html', shell=True)