import win32com.client
import os
import re
import glob
import time
import datetime
import subprocess
#from threading import Thread
import logging

gdrive='\\RevenueAssurance'
script_path=os.path.dirname(os.path.abspath(__file__))
rootf='../../../'
list_for_exec=list()
os.chdir(os.path.join(script_path,'logs'))
logging.basicConfig(filename=('Master_log.log'),format='%(levelname)s : %(asctime)s %(message)s',level=logging.DEBUG)
logging.info(' Master started to run at: '+str(datetime.datetime.now()))
alltasks=list()
prev_tmp='root'
class OneTask(object):
    amount=0
    def __init__(self,filename,stime):
        self.filename=filename
        self.stime=stime
        self.status='scheduled'
        self.prevpid='none'
        self.pid=''
        self.subprogres=0
        self.subtotal=0
        self.amount+=1
    def setStatus(self,status):
        self.status=status
    def setProgres(self,progres):
        self.subprogres=progres
    def setTotal(self,total):
        self.subtotal=total
    def setPid(self,i):
        self.pid=i
    def setPrevPid(self,i):
        self.prevpid=i

def createDeamons(i):
    global alltasks
    global prev_tmp
    print 'Running deamon..'
        
    try:
        os.chdir(script_path)
        logging.info('-Running the deamon')
        i.setStatus('waiting')
        command1 = subprocess.call(['python ', 'slave_deamon.py ',i.filename,'1','root'])
        i.setPid('root')    
        i.setPrevPid('root')    
        logging.info('-deamon '+str(i.filename)+' executed' )
        prev_tmp=i.pid
     
    except:
        print 'cannot create deamon'
        logging.info('-cannot execute deamon')  
  

def getFiles():
    i=0
    global alltasks
    regP=r'file=<(.+)>\s+time=<(\d{1,2}:\d{1,2})>'
    todayf=datetime.datetime.now().strftime("%Y.%m.%d")
    lines=[]
    matchObj=''
    logging.info('-Trying to open config file')
    with open('files.cfg') as dirs:
        lines=dirs.readlines()
    for line in lines:
        matchObj=re.match(regP,unicode(line).replace('"',"'"))
        if matchObj:
            stime=matchObj.group(2)
            date = datetime.datetime(*(time.strptime(todayf+' '+stime,'%Y.%m.%d %H:%M')[0:6]))
            list_for_exec.append((i,matchObj.group(1),date))
            alltasks.append(OneTask(matchObj.group(1),date))
            i+=1
            logging.info('-- adding to schedule: '+str(i)+' '+ matchObj.group(1)+' at: '+str(date))
    dirs.close()
    return list_for_exec

def callMacro(pfile):
    changeFiles(pfile)
    fileName = os.path.basename(pfile)
    print fileName
    folderf=os.path.dirname(pfile)
    print folderf
    os.chdir(os.path.join(rootf,folderf))
    current_dir=os.path.dirname(os.path.abspath(__file__))
    
    try:
        xl=win32com.client.Dispatch("Excel.Application")
        xl.Visible = True
    except:
        print 'cannot open Excel'+ fileName
    
    try:
        xl.Workbooks.Open(os.path.join(current_dir,fileName))
        workbook = xl.ActiveWorkbook
    except:
        print 'cannot open '+ fileName
    try:
        xl.Application.Run(fileName+"!PT.PT")
    except:
        print 'cannot run Macro in '+ fileName
    try:
        workbook.Close(True)
      
    except:
        print 'cannot save '+ fileName
    try:
        xl.Application.Quit()
    except:
        print 'cannot quit '+ fileName
    del xl

def isExcelRunning():
    try:
        excel = win32com.client.GetActiveObject("Excel.Application")
        return 1
    except:
        return 0

def localDeamon(schedFiles):
    a=len(schedFiles)
    while a>0:
        print 'waiting...'
        for i in alltasks:
            now=datetime.datetime.now()
            if i.stime<now and i.status=='scheduled':
                logging.info('Trying to start deamon for '+i.filename)
                try:
                    createDeamons(i)
                    logging.info('Deamon executed with success')
                    time.sleep(5)
                    a-=1
                except:
                    logging.info('Deamon cannot be executed')
                                    
        time.sleep(60)
      
            
def getProgres(schedFiles):
    for i,eachfile,stime in schedFiles:
        fileName ='updating_'+ str(os.path.basename(eachfile))
        folderf=os.path.dirname(eachfile)
        os.chdir(os.path.join(rootf,folderf))
        current_dir=os.path.dirname(os.path.abspath(__file__))
        
os.chdir(script_path)
schedFiles=getFiles()
logging.info('Scheduled with success')
print "scheduled with success"
localDeamon(alltasks)
import sys
sys.exit()