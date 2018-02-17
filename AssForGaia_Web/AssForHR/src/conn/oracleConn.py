import src.main.tools.sourceRead as sourceRead
import os
import src.main.tools.readConfig as readConfig



# def oracleConn():
dbsource = sourceRead.readConn()
print(dbsource.getInfo())
# path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))
config_path = readConfig.ConfigPath()
path = config_path.getWebAssforhrPath()
print(path)

