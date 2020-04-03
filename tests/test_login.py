import pytest
from base.method import Requests
from utils.operationYaml import OperationYaml
import json

obj=Requests()
objYaml=OperationYaml()

@pytest.mark.parametrize('datas',objYaml.readYaml())
def test_login(datas):
    # print(datas['data'])
    # print(type(datas['data']))
    # print(datas['expected'])
    # print(type(datas['expected']))
    r=obj.post(url=datas['url'],json=datas['data'])
    # print(r.text)
    # print(json.dumps(r.json(),ensure_ascii=False))
    # print(type(json.dumps(r.json(),ensure_ascii=False)))
    assert datas['expected'] in json.dumps(r.json(),ensure_ascii=False)

if __name__=='__main__':
    pytest.main('-s','-v','test_login.py')