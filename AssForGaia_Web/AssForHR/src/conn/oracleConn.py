import src.main.tools.sourceRead as sourceRead
import os

# def oracleConn():
dbsource = sourceRead.readConn()
print (dbsource.getInfo())
# path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))
path = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
print(path)

