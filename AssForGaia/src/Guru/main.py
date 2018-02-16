#encoding:utf8
import tkinter as tk #用于窗口界面设计
import sys
import tkinter.messagebox as mb #用于在窗口中创建messagebox
import os #os.urandom用于随机生成秘钥key
import pymssql
import pymssql #用于连接mssql数据库
from argcomplete.compat import str
from twisted.conch.test.test_helper import HEIGHT
from openpyxl.styles.borders import Side
import codecs #用于查看编码格式
from PRPCRYPT import prpcrypt #调用加密算法，用于加密数据库链接中的密码
import GAIAMDC
#from Guru.GAIAMDC import addNewTmpl,queryTmpl,addTmplVar,dictQueryTmplVars,addNewTask,queryTaskbyTmpl,addMainDataSource,addSubDataSource,dictQuerySubDataSourceList,readDocument,listVariableMappingByTaskId,listRecipientVarsByTmpId,addVarMapping,addRecipient,addTmplContent#调用邮件配置模块，用于配置邮件提醒
#from GAIAPAYROLL import * #调用薪资配置模块，用于薪资公式处理
#import PayrollCal as PayrollCal
import json #json数据格式，用于写入数据库链接配置信息
import random
import string
from odo.backends.tests.test_json import json_file
from tkinter.messagebox import showinfo
from _codecs import encode
import urllib.request
import http.cookiejar as cookielib
import urllib.parse
from html.parser import HTMLParser
import html
import cchardet as chardet#获取指定页面的编码方式
from _codecs import decode
import gzip
import bs4 as bs
import re
import math
import copy
import http.client as httplib
#快速请求
import httplib2

rootfile=r'E:\KM\GITPROJECT\HumanResourcesAss\AssForGaia'
rootWorkSapce =r'E:\workspace\tmpfileAssForGaia'
cookie = cookielib.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
CookieOpener = urllib.request.build_opener(handler)
headers = {}
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
headers['Accept-Encoding'] = 'deflate'
headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
headers['Connection'] = 'keep-alive'
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'

def addWord(theIndex,word,pagenumber): 
    theIndex.setdefault(word, [ ]).append(pagenumber)#存在就在基础上加入列表，不存在就新建个字典key 
def randomString(n):
    return (''.join(map(lambda xx:(hex(ord(xx))[2:]),''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',n)).replace(" ",""))))[0:16]  
def readConn():
    dbConn = DBSource(r'peter',r'sa',r'111111',r'gaia')
    if os.path.exists('./sourcename.json'):
        if os.path.getsize('./sourcename.json'):
            with open('./sourcename.json') as connFile:
                readConnDict = json.load(connFile)
                decrypt_tmpkey = prpcrypt(readConnDict['dbsalt'])
                decrypt_psw = decrypt_tmpkey.decrypt(readConnDict['dbpsw'])
                dbConn = DBSource(readConnDict['servername'],readConnDict['dbusername'],decrypt_psw,readConnDict['dbname'])
    return dbConn
def dictReadSource():
    readSource = {}
    readSource['webpsw'] = r'111111'
    readSource['rooturl'] = r'http://peter/zybxehr'
    readSource['host'] = r'peter'
    readSource['port'] = r'80'
    readSource['webname'] = r'sa'
    readSource['websalt'] = r'111111'      
    if os.path.exists('./websource.json'):
        if os.path.getsize('./websource.json'):
            with open('./websource.json') as sourceFile:
                readSourceDict = json.load(sourceFile)
                decrypt_webtmpsalt = readSourceDict.get('websalt')
                print('decrypt_webtmpsalt: %s'%(decrypt_webtmpsalt))
                decrypt_webtmpkey = prpcrypt(decrypt_webtmpsalt)
                decrypt_tmpwebpsw = readSourceDict.get('webpsw')
                print('decrypt_tmpwebpsw: %s'%(decrypt_tmpwebpsw))
                decrypt_webpsw = decrypt_webtmpkey.decrypt(decrypt_tmpwebpsw)
                print('decrypt_webpsw: %s'%(decrypt_webpsw))
                readSource['webpsw'] = decrypt_webpsw
                readSource['rooturl'] = readSourceDict.get('rooturl')
                readSource['host'] = readSourceDict.get('host')
                readSource['port'] = readSourceDict.get('port')
                readSource['webname'] = readSourceDict.get('webname')       
    return readSource       
#ehr = DBSource("localhost","sa","1qaz2wsx","ZYBXSCeHR_DB_170207")   
class DBSource:
    def __init__(self,servername,dbusername,dbpsw,dbname):
        self.servername = servername
        self.dbusername = dbusername
        self.dbpsw = dbpsw
        self.dbname = dbname
class UrlRequest:
    def __init__(self,rooturl,cookie,headers,host,port,loginurl,webname,webpsw,CookieOpener):
        self.rooturl = rooturl
        self.cookie = cookie
        self.headers = headers
        self.host = host
        self.port = port
        self.loginurl = loginurl
        self.webname = webname
        self.webpsw = webpsw  
        self.CookieOpener = CookieOpener                              
def connWithDB (DBSource,orderNeed):   
    conn=pymssql.connect(DBSource.servername,DBSource.dbusername,DBSource.dbpsw,database=DBSource.dbname)
    DBlist = []
    cursor=conn.cursor()    
    cursor.execute(orderNeed)
    row=cursor.fetchone()
    while row:
        #print("readline:%s"%(row[0]))
        DBlist.append(row[0])
        row=cursor.fetchone()
    conn.commit()    
    conn.close()
    return DBlist
def connWithDBWithnoresult (DBSource,orderNeed):    
    conn=pymssql.connect(DBSource.servername,DBSource.dbusername,DBSource.dbpsw,database=DBSource.dbname)
    cursor=conn.cursor()    
    cursor.execute(orderNeed)
    conn.commit()
    conn.close()
#调整窗口位置居中
'''
def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()

def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()
'''
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    width, height = root.maxsize() #把窗口重写成了最大
    size = '%dx%d+%d+%d' % (width, height-65,-10 ,0 )#print (size)
    root.geometry(size)
class Hide():
    def __init__(self,Master):
        Master.withdraw()         
def quit_all():
    sys.exit(0)
class Show():
    def __init__(self,Master):
        Master.update()
        Master.deiconify()
def writeToTxt(truepath,filecontent):
    fileobject = open(truepath,'w')
    for item in (filecontent):
        fileobject.write(item)
    fileobject.close() 
def readFromTxt(truepath):
    fileobject = open(truepath,'rb')
    fileReadContent = fileobject.read().decode('utf-8')
    fileobject.close()
    return  fileReadContent  
def checkConn():
    try:
        selectTest = """select 1 from PSNACCOUNT"""
        db_test = connWithDB(ehr,selectTest)
    except(Exception):
        mb.showinfo('请配置正确的数据连接')   
def mssql_checkUserObjectExist(UserObjectname):
    testSql = """DECLARE @result INT,@objname nvarchar(776);\n set @result = 0;\n set @objname = '""" + UserObjectname +"""';\n IF  EXISTS (SELECT 1 FROM sys.objects WHERE object_id in (object_id(@objname))) \n begin;\n set @result = 1;\n end; \n select @result; """ 
    db_test = connWithDB(ehr,testSql)
    return db_test
def getpermanentID(rooturl,headers,loginurl): 
    req = urllib.request.Request(url = loginurl,headers = headers)
    response = urllib.request.urlopen(req)
    soup = bs.BeautifulSoup(response.read().decode(),"lxml")
    permanentID = soup.form.find(id="permanentId")["value"]
    return permanentID
def requestNeedurl(needurl,postData,headers,CookieOpener):
    needurl = needurl
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' 
    if headers.get('Content-Type') == None:
        pass
    else:
        del headers['Content-Type']
    encodepostData = urllib.parse.urlencode(postData).encode('utf-8')
    req = urllib.request.Request(url = needurl,data = encodepostData,headers = headers)
    response = CookieOpener.open(req)
    return response
def requestNeedurlByJsonPost(needurl,postData,headers,cookie,host,port):
    needurl = needurl
    fullcookies = ''
    for item in cookie:
            singlecookie = item.name + '=' + item.value + ';'
            fullcookies = fullcookies + singlecookie
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Cookie'] = fullcookies
    conn = httplib.HTTPConnection(host,port)
    conn.request("POST", needurl, json.JSONEncoder().encode(postData), headers)
    response = conn.getresponse()
    return response
def loginInSystem(requestInfo):
    permanentID = getpermanentID(rooturl=requestInfo.rooturl,headers=headers,loginurl=requestInfo.loginurl)
    postData = {'account':requestInfo.webname,'password':requestInfo.webpsw,'cultureCode':'zh-CN','permanentId':permanentID}
    print('requestInfo.loginurl:%s'%(requestInfo.loginurl))
    response = requestNeedurl(needurl  = requestInfo.loginurl ,postData = postData,headers = headers,CookieOpener = requestInfo.CookieOpener)
    return response
def loginInSystem_resCookie(requestInfo):
    permanentID = getpermanentID(rooturl=requestInfo.rooturl,headers=headers,loginurl=requestInfo.loginurl)
    postData = {'account':requestInfo.webname,'password':requestInfo.webpsw,'cultureCode':'zh-CN','permanentId':permanentID}
    print('requestInfo.loginurl:%s'%(requestInfo.loginurl))
    response = requestNeedurl(needurl  = requestInfo.loginurl ,postData = postData,headers = headers,CookieOpener = requestInfo.CookieOpener)
    return response,cookie
def endOfDef():
    pass
       
class Create_main_window:  
    
    def __init__(self,Master):
        #pub.subscribe(self.listener, "otherFrameClosed")
        center_window(Master, 1366, 768)  # 设置窗口居中，设置宽度和高度       
        Master.title("BenQGuru eHR Ass For Gaia7303")
        Master.resizable(True, True)
        Master.protocol("WM_DELETE_WINDOW", quit_all)
                
        #********--------初始化2 爬取薪资信息功能块初始化数据区域
        #创建WebRequest默认值
        self.rooturl=ehrsource.get('rooturl') #请求登录页面的刷新ID时使用
        self.hosturl=self.rooturl + r'/account/logon?' #登录页面
        self.loginurl = self.rooturl + r'/account/logon?'
        self.host = ehrsource.get('host')
        self.port = ehrsource.get('port')
        self.webname = ehrsource.get('webname')
        self.webpsw = ehrsource.get('webpsw')
        #创建其他默认值
        self.Simulateurl =self.rooturl + r'/Account/SimulateLogon' #模拟登录页面
        #创建初始化对象
        self.tabledatainDict = {} #读取页面数据用于缓存json数据
        self.tabledatainTh = [] #读取页面数据用于缓存列标题
        self.tabledatainTr = [] #读取页面数据用于环境行记录值
        global WebRequest
        WebRequest = UrlRequest(rooturl=self.rooturl,cookie = cookie,headers = headers,host = self.host,port = self.port,loginurl = self.loginurl,webname = self.webname,webpsw = self.webpsw,CookieOpener = CookieOpener)
        #创建框架
        self.mainframe=tk.Frame(Master)#用于拜访主按钮
        self.CONframe=tk.Frame(Master)#用于更新数据库链接
        self.operationArea = tk.Frame(Master)        
        #CONframe数据连接框架，用于更新数据库链接
            #用于生成数据库链接区块的标签
        self.label_titleConnection = tk.Label(self.CONframe,text='加载数据库配置')
        self.label_sourcename = tk.Label(self.CONframe,text='数据源名称')
        self.label_servername = tk.Label(self.CONframe,text='服务器名称')
        self.label_dbname = tk.Label(self.CONframe,text='数据库名')
        self.label_dbusername = tk.Label(self.CONframe,text='用户名')
        self.label_dbpsw = tk.Label(self.CONframe,text='用户密码')  
        self.label_rooturl = tk.Label(self.CONframe,text='站点根目录')
        self.label_host = tk.Label(self.CONframe,text='主机')
        self.label_port = tk.Label(self.CONframe,text='端口')
        self.label_webname = tk.Label(self.CONframe,text='账户')
        self.label_webpsw = tk.Label(self.CONframe,text='密码')       
            #用于生成数据库链接区块的文本框的变量
        self.entry_sourcename_var = tk.StringVar()
        self.entry_servername_var = tk.StringVar()
        self.entry_dbname_var = tk.StringVar()
        self.entry_dbusername_var = tk.StringVar()
        self.entry_dbpsw_var = tk.StringVar()
        self.entry_rooturl_var = tk.StringVar()
        self.entry_host_var = tk.StringVar()
        self.entry_port_var = tk.StringVar() 
        self.entry_webname_var = tk.StringVar() 
        self.entry_webpsw_var = tk.StringVar()     
            #用于生成数据库链接区块的文本框    
        self.entry_sourcename = tk.Entry(self.CONframe,textvariable=self.entry_sourcename_var)
        self.entry_servername = tk.Entry(self.CONframe,textvariable=self.entry_servername_var)
        self.entry_dbname = tk.Entry(self.CONframe,textvariable=self.entry_dbname_var)
        self.entry_dbusername = tk.Entry(self.CONframe,textvariable=self.entry_dbusername_var)
        self.entry_dbpsw = tk.Entry(self.CONframe,textvariable=self.entry_dbpsw_var) 
        self.entry_rooturl = tk.Entry(self.CONframe,textvariable=self.entry_rooturl_var) 
        self.entry_host = tk.Entry(self.CONframe,textvariable=self.entry_host_var) 
        self.entry_port = tk.Entry(self.CONframe,textvariable=self.entry_port_var)
        self.entry_webname = tk.Entry(self.CONframe,textvariable=self.entry_webname_var)
        self.entry_webpsw = tk.Entry(self.CONframe,textvariable=self.entry_webpsw_var) 
                      
            #用于向数据库链接区块的文本框列表插入默认值
        self.entry_sourcename.insert(-1,"ehr")
        self.entry_servername.insert(-1,ehr.servername)
        self.entry_dbname.insert(-1,ehr.dbname)
        self.entry_dbusername.insert(-1,ehr.dbusername)
        self.entry_dbpsw.insert(-1,"")
        if ehrsource.get('rooturl') == None:
            self.entry_rooturl.insert(-1,'')
        else:
            self.entry_rooturl.insert(-1,ehrsource.get('rooturl'))           
        if ehrsource.get('host') == None: 
            self.entry_host.insert(-1,'')
        else:      
            self.entry_host.insert(-1,ehrsource.get('host'))
        if ehrsource.get('port') == None:
            self.entry_port.insert(-1,'')
        else:
            self.entry_port.insert(-1,ehrsource.get('port'))
        if ehrsource.get('webname') == None: 
            self.entry_webname.insert(-1,'')
        else:      
            self.entry_webname.insert(-1,ehrsource.get('webname')) 
            #用于向数据库链接区块添加保存数据库链接的按钮
        self.but_saveNewConn = tk.Button(self.CONframe,text='更新链接',command=self.saveNewConnecttion)
        self.but_saveNewSource = tk.Button(self.CONframe,text='更新源',command=self.saveNewSource)
        
        #Master.iconbitmap('E:\工作文档\1608-中银\98客户环境\eHR\Web\Content\images\home\logo-gaia.png')        
#窗口滚动问题没解决 mainScrolly=tk.Scrollbar(Master)  mainScrolly.pack(side="right",fill="y") #mainScrolly.grid(row=22,column=1,sticky=tk.W)  scrolly.config(command=lb.yview)        
        #mainframe框架放置页面主要按钮
            #加载资源区块标签
        self.label_loadResource = tk.Label(self.mainframe,text='加载资源') 
        self.label_payrollOption = tk.Label(self.mainframe,text='薪资公用代码')
        self.label_mainlogicOption = tk.Label(self.mainframe,text='薪资主逻辑')
        self.label_patternOption = tk.Label(self.mainframe,text='计薪模式') 
            #加载资源区块更新数据按钮
        self.lb_mainlogic = tk.Listbox(self.mainframe,selectmode="browse",height=4) 
        self.lb_patternName = tk.Listbox(self.mainframe,selectmode="browse",height=4)
        
        self.label_title_bpmConfig = tk.Label(self.mainframe,text='工作流配置')
        self.label_showaAllSP = tk.Label(self.mainframe,text='子流程阶段调用中的sp')
        scrolly_showALLSP=tk.Scrollbar(self.mainframe,orient="vertical")      
        self.lb_bpm_showAllSP = tk.Listbox(self.mainframe,selectmode="browse",yscrollcommand=scrolly_showALLSP.set)   
        scrolly_showALLSP.config(command=self.lb_bpm_showAllSP.yview)
                                                     
        self.but_reoption = tk.Button(self.mainframe,text='加载公用代码',command=self.readPublicCode)
        #operationArea 操作区块的控件
            #读取系统所有签核阶段涉及的sp
        self.label_option = tk.Label(self.operationArea,text='根据上方显示的列表写入文件')
        self.entry_rootfile_var = tk.StringVar()        
        self.entry_rootfile = tk.Entry(self.operationArea,textvariable=self.entry_rootfile_var)
        self.entry_rootfile.insert(0,"E:\\workspace\\tmpfile")
        self.but_readShowAllSP = tk.Button(self.operationArea, text="点击读取SP", width=10,command=lambda:self.readShowALLSP(db_ShowALLSP))#   

        self.label_readMdcDoc = tk.Label(self.operationArea,text='读取下方的邮件提醒模板规格文件')
        self.entry_mdcFilePath_var = tk.StringVar()        
        self.entry_mdcFilePath = tk.Entry(self.operationArea,textvariable=self.entry_mdcFilePath_var)
        self.entry_mdcFilePath.insert(0,r'E:\工作文档\1608-中银\07解决方案\T0801中银_邮件提醒开发规格书_PES_V1.2_170522.docx')
        self.but_writeMdcFileToWeb = tk.Button(self.operationArea, text="点击读写", width=10,command=lambda:self.writeMdcFileToWeb())

        
            #配置薪资调试公用信息并跳转至详细调试页面
        self.but_createPayrollcalWindow = tk.Button(self.operationArea,text='点击跳转到薪资调试页面',command=lambda:self.show_win_PayrollCal())


        self.but_knockDoorforRequest = tk.Button(self.operationArea,text='登录系统',command=lambda:self.knockDoor())
        
        self.entry_singleWorkNo_var = tk.StringVar()
        self.entry_singlePackageID_var = tk.StringVar()        
        self.entry_allCalPackageID_var = tk.StringVar() 
        self.text_singleCalDebug_var = tk.StringVar()
        self.text_singleCalDebug_var.set('未加载')
        self.entry_singleCalDebug_var = tk.StringVar()
        self.entry_singleCalDebug_var.set('未加载')        
        
        self.label_title_AllCal = tk.Label(self.operationArea,text='全部薪资调试')
        self.label_allCalPackageID = tk.Label(self.operationArea,text='调试薪资包ID') 
        self.entry_allCalPackageID = tk.Entry(self.operationArea,textvariable=self.entry_allCalPackageID_var)       
        self.label_title_singleCal = tk.Label(self.operationArea,text='单人薪资调试')
        self.label_singlePackageID = tk.Label(self.operationArea,text='调试薪资包ID') 
        self.entry_singlePackageID = tk.Entry(self.operationArea,textvariable=self.entry_singlePackageID_var) 
        self.label_singleWorkNo = tk.Label(self.operationArea,text='调试工号')        
        self.entry_singleWorkNo = tk.Entry(self.operationArea,textvariable=self.entry_singleWorkNo_var)
        self.label_singleCalDebug = tk.Label(self.operationArea,text='单人薪资调试内容')
        self.text_singleCalDebug = tk.Text(self.operationArea,height=8,width=20) 
               
        self.entry_allCalPackageID.insert(0,'5d2d7fab-49f2-4ed0-ae24-f35d7bc53c3c')
        self.entry_singleWorkNo.insert(0,'0006061')
        self.entry_singlePackageID.insert(0,'5d2d7fab-49f2-4ed0-ae24-f35d7bc53c3c')
                        
        self.but_requestForAllCalData = tk.Button(self.operationArea,text='读取全部调试数据',command=lambda:self.requestAllCalData())
                
        self.but_requestForSingleData = tk.Button(self.operationArea,text='读取指定调试数据',command=lambda:self.requestSingleCalData())
        
        self.entry_subjectNameToClear_var = tk.StringVar()
        self.label_title_subjectNameToClear = tk.Label(self.operationArea,text='清除指定薪资科目的公式')
        self.label_subjectNameToClear = tk.Label(self.operationArea,text='薪资科目名称（可为空）')
        self.entry_subjectNameToClear = tk.Entry(self.operationArea,textvariable=self.entry_subjectNameToClear_var) 
        self.but_clearSubjectFormual = tk.Button(self.operationArea,text='清除公式',command=lambda:self.clearPayrollFormual())
        
#页面布局位置
        #connframe布局位置
        self.label_titleConnection.grid(row=0,column=0,sticky=tk.W)
        self.label_servername.grid(row=1,column=3,sticky=tk.W)
        self.label_dbusername.grid(row=2,column=1,sticky=tk.W)
        self.label_dbpsw.grid(row=2,column=3,sticky=tk.W)   
        self.label_dbname.grid(row=1,column=5,sticky=tk.W)  
        self.label_sourcename.grid(row=1,column=1,sticky=tk.W)
        self.label_rooturl.grid(row=1,column=7,sticky=tk.W)
        self.label_host.grid(row=1,column=9,sticky=tk.W)
        self.label_port.grid(row=2,column=9,sticky=tk.W)
        self.label_webname.grid(row=1,column=11,sticky=tk.W)
        self.label_webpsw.grid(row=2,column=11,sticky=tk.W)        
                 
        self.entry_servername.grid(row=1,column=4,sticky=tk.W+tk.E)
        self.entry_dbusername.grid(row=2,column=2,sticky=tk.W+tk.E)
        self.entry_dbpsw.grid(row=2,column=4,sticky=tk.W+tk.E)
        self.entry_dbname.grid(row=1,column=6,sticky=tk.W+tk.E)
        self.entry_sourcename.grid(row=1,column=2,sticky=tk.W+tk.E)
        self.entry_rooturl.grid(row=1,column=8,sticky=tk.W+tk.E)
        self.entry_host.grid(row=1,column=10,sticky=tk.W+tk.E)
        self.entry_port.grid(row=2,column=10,sticky=tk.W+tk.E)
        self.entry_webname.grid(row=1,column=12,sticky=tk.W+tk.E)
        self.entry_webpsw.grid(row=2,column=12,sticky=tk.W+tk.E)
             
        self.but_saveNewConn.grid(row=2,column=6,sticky=tk.W+tk.E)
        self.but_saveNewSource.grid(row=2,column=8,sticky=tk.W+tk.E)
        
        #mainframe布局位置
        self.label_loadResource.grid(row=0,column=0,sticky=tk.W) 
        self.but_reoption.grid(row=0,column=1,sticky=tk.W+tk.E)       
        self.label_payrollOption.grid(row=11,column=0,sticky=tk.W)
        self.label_mainlogicOption.grid(row=12,column=0,sticky=tk.W)
        self.label_patternOption.grid(row=12,column=1,sticky=tk.W)      
        self.lb_mainlogic.grid(row=13,column=0)    
        self.lb_patternName.grid(row=13,column=1) 
        self.label_title_bpmConfig.grid(row=20,column=0,sticky=tk.W) 
        self.label_showaAllSP.grid(row=21,column=0,sticky=tk.W)                
        scrolly_showALLSP.grid(row=22,column=1,sticky=tk.N+tk.S+tk.W)  
        self.lb_bpm_showAllSP.grid(row=22,column=0)                 
        #operationArea布局位置                       
        self.label_option.grid(row=0,column=0,sticky=tk.W)
        self.entry_rootfile.grid(row=1,column=0,sticky=tk.W+tk.E)
        self.but_readShowAllSP.grid(row=2, column=0,sticky=tk.W+tk.E+tk.N)
        self.but_createPayrollcalWindow.grid(row=0,column=2,sticky=tk.W+tk.E)
        
        self.label_readMdcDoc.grid(row=3,column=0,sticky=tk.W)
        self.entry_mdcFilePath.grid(row=4,column=0,sticky=tk.W+tk.E)
        self.but_writeMdcFileToWeb.grid(row=5, column=0,sticky=tk.W+tk.E+tk.N)    

        self.but_knockDoorforRequest.grid(row=0,column=2,sticky=tk.W+tk.E)
        
        self.label_title_AllCal.grid(row=1,column=1,sticky=tk.W)
        self.label_allCalPackageID.grid(row=2,column=1,sticky=tk.W)
        self.entry_allCalPackageID.grid(row=2,column=2,sticky=tk.W+tk.E)
        self.but_requestForAllCalData.grid(row=5,column=2,sticky=tk.W+tk.E) 
        
        self.label_title_singleCal.grid(row=1,column=3,sticky=tk.W)
        self.label_singlePackageID.grid(row=2,column=3,sticky=tk.W)
        self.entry_singlePackageID.grid(row=2,column=4,sticky=tk.W+tk.E)
        self.label_singleWorkNo.grid(row=3,column=3,sticky=tk.W)
        self.entry_singleWorkNo.grid(row=3,column=4,sticky=tk.W+tk.E)       
        self.but_requestForSingleData.grid(row=5,column=4,sticky=tk.W+tk.E)
        self.label_singleCalDebug.grid(row=1,column=5,sticky=tk.W)   
        self.text_singleCalDebug.grid(row=2,rowspan=4,column=5,sticky=tk.W+tk.E)    
        
        self.label_title_subjectNameToClear.grid(row=1,column=7,sticky=tk.W)
        self.label_subjectNameToClear.grid(row=2,column=7,sticky=tk.W)
        self.entry_subjectNameToClear.grid(row=2,column=8,sticky=tk.W+tk.E)
        self.but_clearSubjectFormual.grid(row=5,column=8,sticky=tk.W+tk.E)
        
        
          

        #设置frame框架位置
        self.CONframe.place(x=0,y=0)
        self.mainframe.place(x=0,y=100)
        self.operationArea.place(x=0,y=500)
    def selectText(self, event):  
        self.text_singleCalDebug.tag_add(tk.SEL, "1.0", tk.END)        
    def readPublicCode(self):
        main_window.lb_mainlogic.delete(0,)
        main_window.lb_patternName.delete(0,)
        main_window.lb_bpm_showAllSP.delete(0,)
        
        lb_public_data = connWithDB(ehr,"""select mainlogicname from PAYCALCULATEMAINLOGIC""")    
        for item in lb_public_data:
            main_window.lb_mainlogic.insert(0,item)

        lb_public_data = connWithDB(ehr,"""SELECT PATTERNNAME FROM PAYACCOUNTPATTERN WHERE ISDELETED=0""")    
        for item in lb_public_data:
            main_window.lb_patternName.insert(0,item)
            
        lb_public_data = connWithDB(ehr,"""select sp_name from gbpm.fm_mdprocedure""") 
        global db_ShowALLSP 
        db_ShowALLSP = lb_public_data   
        for item in lb_public_data:
            main_window.lb_bpm_showAllSP.insert(0,item)        
        mb.showinfo("Message","公用代码已刷新")
    def writeMdcFileToWeb(self):
        truepath = str(self.entry_mdcFilePath_var.get())
        listParagraphData = readDocument(truepath=truepath) 
        print('listParagraphData:%s'%(listParagraphData))
        loginInSystem(requestInfo = WebRequest)
        for singleParagraphData in listParagraphData:
            #print('singleParagraphData:%s'%(singleParagraphData))
            tmpName = singleParagraphData.get('邮件提醒模板设定').get('模板名称')
            print('tmpName:%s'%(tmpName))
            cookie = WebRequest.cookie
            for item in cookie:
                singlecookie = item.name + '=' + item.value + ';'
                print('singlecookie:%s'%(singlecookie))
            
            #测试通过：功能1：新增模板到人事业务模块下，指定name即可
            resAddNewTmpl = addNewTmpl(name=tmpName,requestInfo = WebRequest)
            #测试通过：功能2：查询指定名称的tmplid列表
            tmplId = [singleTmpl['id'] for singleTmpl in queryTmpl(requestInfo = WebRequest) if singleTmpl['name'] == tmpName]            
            #测试通过：功能4：添加变量到指定tmpid的模板下,add new var to new var list and add  
            listAddNewVars = singleParagraphData.get('变量显示名称')
            for singleNewVar in listAddNewVars:
                if tmplId == []:
                    pass
                else:
                    resAddTmpl = addTmplVar(templateId=tmplId[0],name=singleNewVar['name'],code=singleNewVar['code'],requestInfo = WebRequest)
            #测试通过：功能3：查询指定tmpid的模板下的变量列表             
            dictTmplVar = dictQueryTmplVars(tmplId=tmplId[0],requestInfo = WebRequest)        
            #测试通过：功能6：添加任务到指定的模板下
            taskName = tmpName
            resAddNewTask = addNewTask(name=tmpName,tmplId=tmplId[0],requestInfo = WebRequest)
            tmpTaskId = [singleTask['id'] for singleTask in queryTaskbyTmpl(tmplId=tmplId[0],requestInfo=WebRequest) if singleTask['name'] == taskName]
            if len(tmpTaskId) == 0:
                print('Add filed,Please check tmplId exists')
            else:
                print('Add success,taskId is:'%(tmpTaskId))
            #测试通过：功能5，查看指定tmpid对应的task列表
            taskId = [singleTask['id'] for singleTask in queryTaskbyTmpl(tmplId=tmplId[0],requestInfo=WebRequest) if singleTask['name'] == taskName]
            #测试通过:功能6，向指定taskId添加主数据源
            dataSourceName = singleParagraphData.get('主数据源设定').get('dataSourceName')
            sqlStatement = singleParagraphData.get('主数据源设定').get('sqlStatement')
            resAddMainDataSource = addMainDataSource(taskId=taskId[0],name=dataSourceName,sqlStatement=sqlStatement,requestInfo=WebRequest)
            #测试通过：功能7 向指定的taskId添加子数据源
            listAddSubDataSource = singleParagraphData.get('子数据源设定')
            for singleSubDataSource in listAddSubDataSource:
                resAddSubDataSource = addSubDataSource(taskId=taskId[0],name=singleSubDataSource['subDataSourceName'],sqlStatement=singleSubDataSource['subDataSourceSqlStatement'],requestInfo=WebRequest)    
                #print('resAddSubDataSource:%s'%(resAddSubDataSource))
            #测试通过：功能8 向指定的taskId更新变量数据源 
            resAddVarMapping = addVarMapping(taskId=taskId[0],cookie=cookie,requestInfo=WebRequest,singleParagraphData = singleParagraphData)
            #测试通过：功能9 设定接收人，不允许使用群组只能使用子数据源
            listDocRecipientVars = singleParagraphData.get('接收人设定')
            resAddRecipient = addRecipient(tmplId = tmplId[0],cookie = cookie,listDocRecipientVars = listDocRecipientVars,requestInfo=WebRequest)
            
            designSubject = singleParagraphData.get('邮件提醒模板设定').get('主题')
            designContents = singleParagraphData.get('邮件提醒模板设定').get('模板内容')
            print('designSubject%s'%(designSubject))
            print('designContents%s'%(designContents))
            print('tmplId%s'%(tmplId[0]))
            resAddTmplContent = addTmplContent(tmplId = tmplId[0],cookie = cookie,designSubject = designSubject,designContents = designContents,requestInfo=WebRequest)
        pass    
        
    def readShowALLSP(self,db_ShowALLSP):
        mb.showinfo('SP开始提取')
        checkMphelptextExist = mssql_checkUserObjectExist("mp_helptext")
        if checkMphelptextExist[0] == 0:
            truepath = rootfile + '\importproc_mp_helptext.txt'
            spcontent = readFromTxt(truepath).strip('\n')
            connWithDBWithnoresult(ehr,spcontent)
            mb.showinfo("Tips", "We have import mp_helptext for reploace sys.sp_helptext")        
        db_SPContentList = []
        for item in db_ShowALLSP:
            if item[:4] != "gbpm":#print(item[:4])
                item = "gbpm." + item

            strHead = """\n-------------------TIP """+item
            db_SPContentList.append(strHead)
            strHead = """\nIF  EXISTS (SELECT * FROM sys.objects WHERE name = substring('"""+item+"""',6,99))
            \n DROP PROCEDURE """+item+"""\n GO;\n"""
            db_SPContentList.append(strHead)
            
            selectHelptext = """mp_helptext '"""+item+"""'"""
            #print(selectHelptext)
            db_helptext = connWithDB(ehr,selectHelptext)
            for itemtext in db_helptext:
                db_SPContentList.append(itemtext)
                                
            strFoot = """\n GO;"""
            db_SPContentList.append(strFoot)
            
        filename_showALLSP = 'showALLSP.txt'
        filetruepath_showALLSP = str(self.entry_rootfile_var.get())+'/'+filename_showALLSP#print(filetruepath_showALLSP)

        writeToTxt(filetruepath_showALLSP,db_SPContentList) 
        mb.showinfo('SP提取','SP已经成功提取完毕')        
    def saveNewConnecttion(self):              
        connInfo['servername'] = str(self.entry_servername_var.get())
        connInfo['dbusername'] = str(self.entry_dbusername_var.get())
        connInfo['dbpsw'] = self.entry_dbpsw_var.get()
        connInfo['dbname'] = str(self.entry_dbname_var.get())
        connInfo['sourcename'] = str(self.entry_sourcename_var.get())
        
        tempkey = randomString(16)
        pc = prpcrypt(tempkey)
        encryptedKey = pc.encrypt(connInfo['dbpsw'])
        connInfo['dbpsw'] = str(encryptedKey.decode())
        connInfo['dbsalt'] = str(tempkey)
        
        with open('sourcename.json','w+') as file_object:
            json.dump(connInfo,file_object)
            mb.showinfo('您已经成功更新数据库链接', '您所更新的数据库链接信息如下：服务器名称：%s；数据库名称：%s;用户名：%s；'%(connInfo['servername'],connInfo['dbname'],connInfo['dbusername']))
        global ehr 
        ehr = readConn()
    def saveNewSource(self):
        connInfo['rooturl'] = str(self.entry_rooturl_var.get())
        connInfo['host'] = str(self.entry_host_var.get())
        connInfo['port'] = str(self.entry_port_var.get())
        connInfo['webname'] = str(self.entry_webname_var.get())
        connInfo['webpsw'] = str(self.entry_webpsw_var.get())
        
        tempkey1 = randomString(16)
        pc1 = prpcrypt(tempkey1)
        encryptedKey1 = pc1.encrypt(connInfo['webpsw'])
        connInfo['webpsw'] = str(encryptedKey1.decode())
        connInfo['websalt'] = str(tempkey1)
        
        with open('websource.json','w+') as file_object:
            json.dump(connInfo,file_object)
            mb.showinfo('您已经成功更新站点源', '您所更新的站点信息如下：根地址：%s；主机地址：%s；端口：%s；登录账户：%s；'%(connInfo['rooturl'],connInfo['host'],connInfo['port'],connInfo['webname']))
        global ehrsource 
        ehrsource = dictReadSource()
    def show_win_PayrollCal(self):
        if count == 0:
            Hide(root)
            global win_PayrollCal
            win_PayrollCal = tk.Tk()
            global Payrollcal_window
            #Payrollcal_window = Create_Payrollcal_window(win_PayrollCal)
            win_PayrollCal.mainloop
            Show(win_PayrollCal)
        else:
            Hide(root)
            Show(win_PayrollCal)
    def listener(self, arg1, arg2=None):
        self.show()     
    def requestNeedurl(self,needurl,postData,headers):
        needurl = needurl
        encodepostData = urllib.parse.urlencode(postData).encode('utf-8')
        req = urllib.request.Request(url = needurl,data = encodepostData,headers = headers)
        response = self.CookieOpener.open(req)
        return response  
        #f发送第一次请求获得permanentID
    def getpermanentID(self): 
        req = urllib.request.Request(url = self.hosturl,headers = self.headers)
        response = urllib.request.urlopen(req)
        soup = bs.BeautifulSoup(response.read().decode(),"lxml")
        #print(soup)
        permanentID = soup.form.find(id="permanentId")["value"]
        print(permanentID)
        return permanentID
    def knockDoor(self):
        permanentID = self.getpermanentID()
            #进行二次请求登录
            #构造Post数据，使用fiddler抓包包里分析得出。
        postData = {}    
        postData['account'] = self.webname
        postData['password'] = self.webpsw
        postData['returnUrl'] = ''
        postData['cultureCode'] = 'zh-CN'
        postData['permanentId'] = permanentID        
        response = self.requestNeedurl(needurl  = self.loginurl ,postData = postData,headers = self.headers)
        print(response.info()) 
        mb.showinfo('请求结束',response.info()) 
        return response
        #模拟登录函数
    def simulateOtherUser(self,Simulateurl,headers,account):   
        needPostData = {"pageIndex":0,"pageSize":15,"account":account}
        response = self.requestNeedurl('http://peter/zybxehr/Om/User/Query',needPostData,headers)
        jsonlist = json.loads(response.read().decode())
        recordlist = jsonlist['records'][0]['id']
        if recordlist == '':
            mb.showinfo("Message","要模拟的账户不存在")
        else:                
            postData = {'userid':recordlist}
            encodepostData = urllib.parse.urlencode(postData).encode('utf-8')
            req = urllib.request.Request(url = Simulateurl,data =encodepostData,headers = headers)
            res = self.CookieOpener.open(req)
            print('模拟结束，已经模拟登录：'+recordlist)
            return res
    def simulateUser(self,otherUser):
        response = self.simulateOtherUser(self.Simulateurl,self.headers,otherUser)
        print(response.info())
        mb.showinfo('请求结束','请求完成！！！') 
        return response    
    def get_ViewState(self,needurl,headers):
        needPostData = {} 
        response = self.requestNeedurl(needurl=needurl,postData=needPostData,headers = headers) 
        readResponse = response.read().decode()
        readSoup = bs.BeautifulSoup(readResponse,"html.parser")     
        view_input = readSoup.find(id="__VIEWSTATE")      
        return (view_input['value']) 
    def get_ViewStateFromRes(self,readResponse): 
        readSoup = bs.BeautifulSoup(readResponse,"html.parser")    
        view_input = readSoup.find(id="__VIEWSTATE")      
        return (view_input['value']) 
    def clearPayrollFormual(self):
        clearPayrollFormual(ehr) 
    def requestCalList(self,needPostData,needurl):            
        mb.showinfo('请求开始','请求耗时较长，请稍后！！！')
        viewState = self.get_ViewState(headers = self.headers,needurl=needurl)#print(viewState)
        pageSize = '200'
        targetIndex = '1'
        needPostData['__VIEWSTATE'] = viewState
        needPostData['btnSearchStaff'] = '查询'
        needPostData['grdNavigator$ddlPageSize'] = pageSize
        needPostData['grdNavigator$txtPageIndex'] = targetIndex
        response = self.requestNeedurl(needurl=needurl,postData=needPostData,headers = self.headers)
        readResponse = response.read().decode()
        readSoup = bs.BeautifulSoup(readResponse,"html.parser")
        recordTotalNum =readSoup.find(id = 'grdNavigator_lblRecordsCount').string
        totalPagesNum = int(int(recordTotalNum)/int(pageSize)) + 1
        lastPageNum = int(recordTotalNum)%int(pageSize)
        read_tr = readSoup.find('thead').find_all('th')
        for item in read_tr:
            read_tr = item.find('nobr').string
            self.tabledatainTh.append(read_tr) 
        print(self.tabledatainTh)
        for targetIndex in range(totalPagesNum):
            print('targetIndex')
            print(targetIndex)
            print('totalPagesNum')
            print(totalPagesNum)
            
            if targetIndex == int(totalPagesNum) - 1:
                thisPageNum = lastPageNum
            else:
                thisPageNum = int(pageSize)
            print('thisPageNum')
            print(thisPageNum)
            viewState = self.get_ViewStateFromRes(readResponse)
            needPostData = {'__VIEWSTATE':viewState,'grdNavigator$txtPageIndex':str(targetIndex+1)}
            response = self.requestNeedurl(needurl=needurl,postData=needPostData,headers = self.headers) 
            readResponse = response.read().decode()
            readSoup = bs.BeautifulSoup(readResponse,"html.parser")    
            with open('E:/workspace/tmpfile/temptabledata.json','a') as file_object:
                for item in range(thisPageNum):
                    #print(item)
                    itemid = 'ulgridStaff_r_'+str(item)
                    read_tr = readSoup.find(id = itemid)
                    read_tr_nobr = read_tr.find_all('nobr')
                    tabledatainTr = []
                    for item in read_tr_nobr:
                        tabledatainTr.append(str(item.string).replace("\xa0", " ")) 
                    tabledatainDict = {}
                    tabledatainDict = dict(zip(self.tabledatainTh,tabledatainTr))  
                    print(tabledatainDict) 
                    json.dump(obj=tabledatainDict,fp = file_object,ensure_ascii=False,indent=2)
            writefiletxt = "E:\\workspace\\tmpfile\\Readcircle"+ str(targetIndex+1) +".txt"
            writeToTxt(writefiletxt,readResponse) 
            targetIndex +=1
        mb.showinfo('请求结束','系统已经写入完成数据！！！')
    def requestCalDebug(self):          
        payrollInfo['packageID']= str(self.entry_singlePackageID_var.get())
        payrollInfo['workNO'] = str(self.entry_singleWorkNo_var.get())
        if payrollInfo['packageID']=='':
            mb.showerror('读取错误', '未读取到指定薪资包ID')
            pass
        else:
            if payrollInfo['workNO']=='':
                mb.showerror('读取错误', '未读取到指定工号') 
                pass
            else:
                mb.showinfo('请求开始','请求基本参数：薪资包ID：%s;工号：%s'%(payrollInfo['packageID'],payrollInfo['workNO']))  
                needurl = 'http://peter/zybxehr/ePayroll/PayrollPackage/PackageCalculateDebug.aspx?PackageID='+payrollInfo['packageID']
                viewState = self.get_ViewState(headers = self.headers,needurl=needurl)
                if viewState=='':
                    mb.showinfo('读取错误', '未读取到入口页面的页面状态，请先点击登录进行模拟登录')
                else:
                    needPostData = {'__VIEWSTATE':viewState,'txtWorkNO':payrollInfo['workNO'],'BtnDebug':'调试','TxtPackageID':payrollInfo['packageID']}
                    response = self.requestNeedurl(needurl=needurl,postData=needPostData,headers = self.headers)
                    readResponse = response.read().decode()
                    readSoup = bs.BeautifulSoup(readResponse,"html.parser").find(id="txtDebugInfo").string
                    self.text_singleCalDebug.insert(tk.END, readSoup)
                    self.entry_singleCalDebug_var.set(readSoup)                 
                    writeFullPath = rootWorkSapce + '/CalDebug_'+payrollInfo['workNO']+'.txt'
                    writeToTxt(writeFullPath,readSoup)
                    mb.showinfo('请求结束','请求结束，调试信息被回写到如下地址：%s'%(writeFullPath))         
    def requestAllCalData(self):
        payrollInfo['allcalpackageID'] = str(self.entry_allCalPackageID_var.get()) 
        if payrollInfo['allcalpackageID']=='':
            mb.showerror('读取错误', '未读取到指定薪资包ID')
            pass
        else:  
            needurl = 'http://peter/zybxehr/ePayroll/payrollpackage/PackageCalculate.aspx?PACKAGEID='+payrollInfo['allcalpackageID'] 
            needPostData = {'TxtPackageID':payrollInfo['allcalpackageID']}
            self.requestCalList(needPostData,needurl)        
    def requestSingleCalData(self):
        self.requestCalDebug()
    
            
        
        
                           

if __name__ == "__main__":
    connInfo=dict() #变量初始化
    db_patternName = []
    db_ShowALLSP=[]
    payrollInfo = {}
    ehr = readConn()#print('ehr:%s'%(ehr))
    ehrsource = dictReadSource()#print('ehrsource:%s'%(ehrsource)) 
    tabledatainDict = {}
    tabledatainTh = []
    tabledatainTr = []
    
    
    count = 0
    root = tk.Tk()
    main_window = Create_main_window(root)

    root.mainloop()
    

    
    

                  