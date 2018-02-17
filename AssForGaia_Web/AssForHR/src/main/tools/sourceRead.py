import json
from src.main.tools.prpcrypt import prpcrypt
import os
import src.main.tools.readConfig as readConfig  # 从config文件中读取项目路径


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

    def getInfo(self):
        return '<br>Servername:%s;<br>Dbname:%s;<br>Dbusername:%s;'%(self.servername,self.dbname,self.dbusername)


def readConn():
    '''
        readConn from sourcename.json
    '''

    dbConn = DBSource(r'peter', r'sa', r'111111', r'gaia')
    ConfigPath = readConfig.ConfigPath()
    webAssforhrPath = ConfigPath.getWebAssforhrPath()
    sourcenamePath = webAssforhrPath + '/static/config/sourcename.json'
    if os.path.exists(sourcenamePath):
        if os.path.getsize(sourcenamePath):
            with open(sourcenamePath) as connFile:
                readConnDict = json.load(connFile)
                decrypt_tmpkey = prpcrypt(readConnDict['dbsalt'])
                decrypt_psw = decrypt_tmpkey.decrypt(readConnDict['dbpsw'])
                dbConn = DBSource(readConnDict['servername'], readConnDict['dbusername'], decrypt_psw, readConnDict['dbname'])
    else:
        print("not exist!")
    return dbConn