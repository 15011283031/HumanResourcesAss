# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render_to_response
#用于加密算法
from . import PRPCRYPT,main #调用加密算法，用于加密数据库链接中的密码
import random #加密算法中，用于生成随机加密字符串
#JSON数据格式
import json #json数据格式，用于写入数据库链接配置信息

import os #用于检测文件目录是否存在

from django.http import HttpResponseRedirect

#设置随机字符串 默认被 saveNewConnecttion 调用
def randomString(n):
    '''create random string for prpcrypt,only for 16 numbers'''
    return (''.join(map(lambda xx:(hex(ord(xx))[2:]),''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',n)).replace(" ",""))))[0:16]  
class WebSource:
    '''default WebSource 
        properties:rooturl,host,port,webname,webpsw
        setters:ignore;getters:ignore
        match(WebSource)
    '''
    def __init__(self,rooturl,host,port,webname,webpsw):
        self.rooturl = rooturl
        self.host = host
        self.port = port
        self.webname = webname
        self.webpsw = webpsw
    def setRooturl(self,rooturl):
        self.rooturl = rooturl    
    def getRooturl(self):
        return self.rooturl    
    def setHost(self,host):
        self.host = host    
    def getHost(self):
        return self.host 
    def setPort(self,port):
        self.port = port    
    def getPort(self):
        return self.port 
    def setWebname(self,webname):
        self.webname = webname    
    def getWebname(self):
        return self.webname 
    def setWebpsw(self,webpsw):
        self.webpsw = webpsw    
    def getWebpsw(self):
        return self.webpsw 
           
    def match(self,WebSource):
        if self.rooturl == WebSource.rooturl and self.host == WebSource.host and self.port == WebSource.port and self.webname == WebSource.webname and self.webpsw == WebSource.webpsw:
            return True
        else:
            return False
    def getInfo(self):
        return '<br>RootUrl:%s;<br>Host:%s;<br>Port:%s;<br>Webname:%s;'%(self.rooturl,self.host,self.port,self.webname)      
def readWebSource():  
    webConn = WebSource(r'http://peter/zybxehr',r'peter',r'80', r'sa',r'111111')    
    if os.path.exists('./websource.json'):
        if os.path.getsize('./websource.json'):
            with open('./websource.json') as sourceFile:
                readSourceDict = json.load(sourceFile)
                decrypt_webtmpkey = PRPCRYPT.prpcrypt(readSourceDict.get('websalt'))
                decrypt_webpsw = decrypt_webtmpkey.decrypt(readSourceDict.get('webpsw'))
                webConn = WebSource(readSourceDict['rooturl'],readSourceDict['host'],readSourceDict['port'],readSourceDict['webname'],decrypt_webpsw)                      
    return webConn
def classReadWebSouce():
    ''' readConn from sourcename.json
    '''
    webConn = WebSource(r'http://peter/zybxehr',r'peter',r'80', r'sa',r'111111')
    if os.path.exists('./GURU/websource.json'):
        if os.path.getsize('./GURU/websource.json'):
            with open('./GURU/websource.json') as connFile:
                readConnDict = json.load(connFile)
                decrypt_tmpkey = PRPCRYPT.prpcrypt(readConnDict['websalt'])
                decrypt_psw = decrypt_tmpkey.decrypt(readConnDict['webpsw'])
                webConn = WebSource(readConnDict['rooturl'],readConnDict['host'],readConnDict['port'],readConnDict['webname'],decrypt_psw)
    return webConn


#配置新链接
def saveWebSource(request):
    if request.method == "POST": 
        sourceInfo=dict()
        sourceInfo['rooturl'] =  request.POST.get('rooturl')
        sourceInfo['host'] =  request.POST.get('host')
        sourceInfo['port'] =  request.POST.get('port')
        sourceInfo['webname'] =  request.POST.get('webname')
        tempsw =  request.POST.get('webpsw')
    
        tempkey = randomString(16)
        pc = PRPCRYPT.prpcrypt(tempkey)
        encryptedKey = pc.encrypt(tempsw)
        sourceInfo['webpsw'] = str(encryptedKey.decode())
        sourceInfo['websalt'] = str(tempkey)
    
        tmpWebSource = WebSource(sourceInfo.get('rooturl'),sourceInfo.get('host'),sourceInfo.get('port'),sourceInfo.get('webname'),tempsw)
        
        with open('./GURU/websource.json','w+') as file_object:
            json.dump(sourceInfo,file_object)
            
        ehrWebSource = classReadWebSouce()
        webSourceInfo = classReadWebSouce().getInfo() 
        if tmpWebSource.match(ehrWebSource):
            return HttpResponseRedirect("/GURU/main") 
    return HttpResponse(webSourceInfo)

def websourceConfig(request):
    '''request for updateWebSource '''
    return render_to_response('GURU/updateWebSource.html')




