# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render_to_response
#用于加密算法
from . import PRPCRYPT #调用加密算法，用于加密数据库链接中的密码
import random #加密算法中，用于生成随机加密字符串
#JSON数据格式
import json #json数据格式，用于写入数据库链接配置信息

import os #用于检测文件目录是否存在

from django.http import JsonResponse

#设置随机字符串 默认被 saveNewConnecttion 调用
def randomString(n):
    '''create random string for prpcrypt,only for 16 numbers'''
    return (''.join(map(lambda xx:(hex(ord(xx))[2:]),''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',n)).replace(" ",""))))[0:16]  
class DBSource:
    '''default dbsource 
        properties:servername,dbusername,dbpsw,dbname
        setters:setServername(servername),setDbusername(dbusername),setDbpsw(dbpsw),setDbname(dbname)
        getters:getServername(),getDbusername(),getDbpsw(),getDbname()
        match(DBSource)
    '''
    def __init__(self,servername,dbusername,dbpsw,dbname):
        self.servername = servername
        self.dbusername = dbusername
        self.dbpsw = dbpsw
        self.dbname = dbname
    def setServername(self,servername):
        self.servername = servername
    def setDbusername(self,dbusername):
        self.dbusername = dbusername    
    def setDbpsw(self,dbpsw):
        self.dbpsw = dbpsw    
    def setDbname(self,dbname):
        self.dbname = dbname
    def getServername(self):
        return self.servername
    def getDbusername(self):
        return self.dbusername
    def getDbpsw(self):
        return self.dbpsw   
    def getDbname(self):
        return self.dbname  
    def match(self,DBSource):
        if self.servername == DBSource.servername and self.dbusername == DBSource.dbusername and self.dbpsw == DBSource.dbpsw and self.dbname == DBSource.dbname:
            return True
        else:
            return False        
def readConn():
    ''' readConn from sourcename.json
    '''
    dbConn = DBSource(r'peter',r'sa',r'111111',r'gaia')
    if os.path.exists('./GURU/sourcename.json'):
        if os.path.getsize('./GURU/sourcename.json'):
            with open('./GURU/sourcename.json') as connFile:
                readConnDict = json.load(connFile)
                decrypt_tmpkey = PRPCRYPT.prpcrypt(readConnDict['dbsalt'])
                decrypt_psw = decrypt_tmpkey.decrypt(readConnDict['dbpsw'])
                dbConn = DBSource(readConnDict['servername'],readConnDict['dbusername'],decrypt_psw,readConnDict['dbname'])
    return dbConn
#配置新链接  
def saveNewConnecttion(request):
    ''' get website post:servername,dbusername,dbpsw,dbname,sourcename
        write to sourcename.json:servername,dbusername,dbpsw,dbname,sourcename,dbsalt
        return result ['Success','Failed']
    '''    
    connInfo=dict()              
    connInfo['servername'] =  request.GET['servername']
    connInfo['dbusername'] = request.GET['dbusername']
    tempsw = request.GET['dbpsw']
    connInfo['dbname'] = request.GET['dbname']
    connInfo['sourcename'] = request.GET['sourcename']  
    
    tempkey = randomString(16)
    pc = PRPCRYPT.prpcrypt(tempkey)
    encryptedKey = pc.encrypt(tempsw)
    connInfo['dbpsw'] = str(encryptedKey.decode())
    connInfo['dbsalt'] = str(tempkey)
    
    tmpehr = DBSource(connInfo.get('servername'),connInfo.get('dbusername'),tempsw,connInfo.get('dbname'))
    
    with open('./GURU/sourcename.json','w+') as file_object:
        json.dump(connInfo,file_object)

    ehr = readConn()
    if tmpehr.match(ehr):
        result = 'Success'
    else:
        result = 'Failed'
    return HttpResponse(result)

def loginConfig(request):
    return render_to_response('guru/index.html')
