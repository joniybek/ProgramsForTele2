import os,sys
import mysql.connector as mysql
import sqlite3
import time
import threading

INTERNAL_DATABASE_URI = 'mysql://flask:test@localhost:3306/flask'
DATA_DATABASE_URI = 'mysql://test:test@localhost:3306/data'
ORACLE_DATABASE_URI = 'mysql://test:test@localhost:3306/data'
SQLLITE_DATABASE_URI = 'sqlite:///' + 'app.db'

db_internal = mysql.connect(host="localhost", user="flask", passwd="test", db="flask")
db_data = mysql.connect(host="localhost", user="test", passwd="test", db="data")

class Timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)
        
def refreshData(query,controlName,conOx):
    curOx = conOx.cursor()
    curOx.execute(query)
    columns = [i[0] for i in curOx.description]
    columnsTmp =str(columns[0])+"" + " FLOAT(14,4),".join(columns[1:])+" FLOAT(14,4)"
    db.session.execute("CREATE TABLE IF NOT EXISTS '"+controlName+"' ("+columnsTmp+")",bind=db.get_engine(app, 'data'))
    for row in curOx:
        db.session.execute("CREATE TABLE IF NOT EXISTS '"+controlName+"' ("+columnsTmp+")",bind=db.get_engine(app, 'data'))


def runSQL():
    def thread1(arg1, stop_event):
        while(not stop_event.is_set()):
            #similar to time.sleep()
            time.sleep(10)
            print '---'
            pass
    t1_stop= threading.Event()
    t1 = threading.Thread(target=thread1, args=(1, t1_stop))

    time.sleep(3)
    #stop the thread2
    t1_stop.set()

runSQL()






