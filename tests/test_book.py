from  base.method import Requests
from utils.operationYaml import OperationYaml
from utils.operationExcel import OperationExcel
from common.public import *
import pytest
import json

class TestBook:
    excel=OperationExcel()
    obj=Requests()

    def result(self,r,row):
        assert r.status_code==200
        assert self.excel.getExResult(row=row) in json.dumps(r.json(),ensure_ascii=False)

    def test_book_001(self):
        '''获取所有书籍信息'''
        r=self.obj.get(url=self.excel.getReAddress(row=1))
        self.result(r,1)
        # print(r.json())

    def test_book_002(self):
        '''添加书籍'''
        r=self.obj.post(
            url=self.excel.getReAddress(row=2),
            json=self.excel.getJson(row=2))
        bookId=r.json()[0]['datas']['id']
        writeContent(bookId)
        self.result(r,2)

    def test_book_003(self):
        '''查看添加书籍信息'''
        r=self.obj.get(url=self.excel.getReAddress(row=3))
        self.result(r,3)

    def test_book_004(self):
        '''编辑书籍信息'''
        r=self.obj.put(url=self.excel.getReAddress(row=4),json=self.excel.getJson(row=4))
        self.result(r,4)

    def test_book_005(self):
        '''删除书籍信息'''
        r = self.obj.delete(url=self.excel.getReAddress(row=5))
        self.result(r,5)


if __name__=='__main__':
    pytest.main('-s','-v','test_book.py::TestBook')