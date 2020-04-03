import xlrd
from common.public import *
from utils.operationYaml import OperationYaml
import json


class excelValues:
    caseID = "测试用例ID"
    caseModel = "模块"
    caseName = "接口名称"
    caseUrl = "请求地址"
    casePre = "前置条件"
    method = "请求方法"
    paramsType = "请求参数类型"
    params = "请求参数"
    expect = "期望结果"
    isRun = "是否运行"
    headers = "请求头"
    statusCode = "状态码"
    # caseId=0
    # des=1
    # reAddress=2
    # reParam=3
    # reMethod=4
    # exResult=5
    #
    # def caseID(self):
    #     return self.caseId
    #
    # def Description(self):
    #     return self.des
    #
    # def RequestAddress(self):
    #     return self.reAddress
    #
    # def RequestParameters(self):
    #     return self.reParam
    #
    # def RequestMethod(self):
    #     return self.reMethod
    #
    # def ExpectedResult(self):
    #     return self.exResult

class OperationExcel:
    @property
    def getSheet(self):
        book=xlrd.open_workbook(filePath('data','api.xlsx'))
        return book.sheet_by_index(0)

    @property
    def getRows(self):
        return self.getSheet.nrows

    @property
    def getCols(self):
        return self.getSheet.ncols

    # def getValue(self,row,col):
    #     return self.getSheet().cell_value(row,col)
    #
    # def getCaseID(self,row):
    #     return self.getValue(row=row,col=excelValues().caseID())
    #
    # def getReAddress(self,row):
    #     url=self.getValue(row=row,col=excelValues().RequestAddress())
    #     if '{bookID}' in url:
    #         return str(url).replace('{bookID}',readContent())
    #     else:
    #         return url
    #
    # def getReParame(self,row):
    #     return self.getValue(row=row,col=excelValues().RequestParameters())
    #
    # def getJson(self,row):
    #     return self.dictYaml()[self.getReParame(row=row)]
    #
    # def getReMethod(self,row):
    #     return self.getValue(row=row,col=excelValues().RequestMethod())
    #
    # def getExResult(self,row):
    #     return self.getValue(row=row,col=excelValues().ExpectedResult())

    def getExcelDatas(self):
        datas=list()
        title=self.getSheet.row_values(0)
        for item in range(1,self.getRows):
            row_content=self.getSheet.row_values(item)
            datas.append(dict(zip(title,row_content)))
        return datas
        # print(title)

    def runs(self):
        '''获取到可执行用例'''
        run_list=[]
        for item in self.getExcelDatas():
            isRuns=item[excelValues.isRun]
            if isRuns=='y':
                run_list.append(item)
            else:
                pass
        return run_list
            # print(isRuns)

    def case_lists(self):
        '''获取excel里全部测试点'''
        cases=list()
        for item in self.getExcelDatas():
            cases.append(item)
        return cases

    def case_prev(self,casePrev):
        '''
        根据前置测试条件找到关联的前置测试用例
        :param casePrev:前置测试条件
        :return
        '''
        for item in self.case_lists():
            if casePrev in item.values():
                return item
        return None

    def prevHeaders(self,prevResult):
        '''
        替换被关联测试点的请求头变量值
        :param prevResult:
        :return:
        '''
        for item in self.runs():
            headers=item[excelValues.headers]
            if '{token}'in headers:
                headers=str(headers).replace('{token}',prevResult)
                return json.loads(headers)
            # print(headers)


obj=OperationExcel()
for item in obj.case_lists():
    print(item)
# for item in obj.getExcelDatas():
#     print(item[excelValues.caseUrl])
# print(obj.getExcelDatas())
# print(obj.getCaseID(row=4))
# print(obj.getReParame(row=4))
# print(obj.getJson(2))
# print(type(obj.getJson(row=2)))

