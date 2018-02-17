import configparser
import os

config = configparser.RawConfigParser()
current_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
cfg_path = current_path + r'/resources/conf/web.cfg'
config.read(cfg_path)


class ConfigPath:
    # default ConfigPath
    # properties:rootPath,webPath,webAssforhrPath;
    # setters:setRootPath, setWebPath, setWebAssforhrPath;
    # getters:getRootPath, getWebPath, getWebAssforhrPath;
    # getInfo

    def __init__(self):
        self.rootpath = config.get('path2', 'root')
        self.webpath = config.get('path2', 'web')
        self.webassforhrpath = config.get('path2', 'web_assforhr')

    def getWebPath(self):
        return self.webpath

    def setWebAssforhrPath(self, webassforhrpath):
        self.webassforhrpath = webassforhrpath

    def getWebAssforhrPath(self):
        return self.webassforhrpath

    def getInfo(self):
        return '<br>RootPath:%s;<br>WebPath:%s;<br>WebAssforhrPath:%s;' % (
            self.rootpath, self.webpath, self.webassforhrpath)

# getfloat() raises an exception if the value is not a float
# getint() and getboolean() also do this for their respective types



