
# coding: utf-8
import soaplib
import cx_Oracle as cx

from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase
from soaplib.core.service import soap
from soaplib.core.model.clazz import Array
from soaplib.core.model.clazz import ClassModel
from soaplib.core.model.primitive import Integer,String, Double
from soaplib.core import Application

# 数据库交互层，模拟一个简单的数据库交互
class DBManage(ClassModel):
    reqNo       = ''
    paramOut    = []

    def __init__(self, reqNo):
        self.reqNo = reqNo

    def exeQuery(self):
        # Connect to database and query values
        conn = cx.connect('db tns connection string') #填写数据库连接字符串
        conn.begin() #开始事务
        print ("connected")
        cursor = conn.cursor()
        cursor.execute("""select 'Hello!' msg from dual""") #查询示例
        rs = cursor.fetchone()
        rtnMsg = rs[0]
        print (rtnMsg) # Hello!

        self.paramOut = [rtnMsg]

        conn.commit()  #提交事务
        cursor.close() #关闭资源
        conn.close()   #关闭连接


# 请求信息类
class TestRequestInfo(ClassModel):
    __namespace__ = "TestRequestInfo"
    reqNo           = String


# 返回信息类
class ResultInfo(ClassModel):
    __namespace__ = "ResultInfo"
    reqNo         = String
    resMsg        = String

# 请求方法
def exeRules(reqInfo):
    reqNo = reqInfo.reqNo

    # Query Database and get values
    dm = DBManage(reqNo)
    dm.exeQuery()
    rs = dm.paramOut
    print 'dm invoke ok!'

    resInfo = ResultInfo()
    resInfo.reqNo  = reqNo
    resInfo.resMsg = rs[0]

    #print resInfo
    return resInfo


class TestService(DefinitionBase):  #WebService Method
    @soap(TestRequestInfo,_returns=ResultInfo)
    def getResultInfo(self,reqInfo):
        resInfo = ResultInfo()
        resInfo = exeRules(reqInfo)
        #print resInfo
        return resInfo


if __name__=='__main__':
    try:
        print '服务已启动'
        from wsgiref.simple_server import make_server
        soap_application = Application([TestService], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server('localhost', 8899, wsgi_application)
        server.serve_forever()

    except ImportError:
        print 'error'

