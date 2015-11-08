import sys
import time
print 'Deamon is executed '
print 'Arguments: '+str(sys.argv)
import os
import shutil
import logging
import datetime
script_path=os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_path,'logs'))
PID=os.getpid()
logfile='log_'+str(PID)+'.log'
logging.basicConfig(filename=('log_'+str(PID)+'.log'),format='%(levelname)s : %(asctime)s %(message)s',level=logging.DEBUG)
logging.info(' started to run with arguments'+ str(sys.argv))
rootf='../../../'

# check  arguments existance
if len(sys.argv)>2:
    os.chdir(script_path)
    stime=sys.argv[2]
    prevPID=sys.argv[3]
    filename=sys.argv[1]
else:
    logging.debug('Arguments are less than expected')
    sys.exit("Error message")

def isExcelRunning():
    import win32com.client
    try:
        excel = win32com.client.GetActiveObject("Excel.Application")
        return 1
    except:
        return 0

def check_pid(prevPID):
    import ctypes
    logging.debug('-checking PID of previous file')
    kernel32 = ctypes.windll.kernel32
    SYNCHRONIZE = 0x100000

    process = kernel32.OpenProcess(SYNCHRONIZE, 0, prevPID)
    if process != 0:
        kernel32.CloseHandle(process)
        return True
    else:
        return False
  
def changeFiles(fname):
    import ctypes
    import glob
    ATTRIBUTE = 0x02
    TMP='old_upd'
    os.chdir(script_path)
    fileName = os.path.basename(fname)
    FILE_PATTERN='????_????_'
    folderf=os.path.dirname(fname)
    os.chdir(os.path.join(rootf,folderf))
    script_dir=os.path.dirname(os.path.abspath(__file__))
    current_dir=os.getcwd()
    if not os.path.exists(TMP):
        print "path doesnt exists"
        os.makedirs(TMP)
        ctypes.windll.kernel32.SetFileAttributesW.argtypes = (ctypes.c_wchar_p, ctypes.c_uint32)
        ret = ctypes.windll.kernel32.SetFileAttributesW(os.path.join(current_dir,TMP),ATTRIBUTE)
        
    else:
        try:
            print "path exists"
            os.chdir(TMP)
            fliest = [ f for f in glob.glob('*'+fileName)]
            for f in fliest:
                try:
                    os.remove(f)
                except:
                    sys.exc_info()                    
                    pass
        except:
            #print sys.exc_info()[0]
            pass
        os.chdir('..')
    ##find last mod file
    try:
        print 'wildcards'+FILE_PATTERN+fileName
        lexcel=glob.glob(FILE_PATTERN+fileName)
    except:
        logging.debug('cannot find file '+FILE_PATTERN+fileName)
        return ''
    newestfile=max(lexcel, key=lambda p: os.stat(p).st_mtime)
    shutil.copyfile(newestfile, os.path.join(TMP,newestfile))
    if os.path.exists('updating_'+fileName):
        os.remove('updating_'+fileName)
    os.rename(newestfile,'updating_'+fileName)
    return (folderf,'updating_'+fileName)
def changeBack(folderf,fname):
    logging.info('--trying rename update_ file')
    NOW=datetime.datetime.today().strftime("%m%d_%H%M_")
    os.chdir(script_path)
    os.chdir(os.path.join(rootf,folderf))
    try:
        os.rename(fname,NOW+fname[9:])
    except:
        logging.debug('--cannot rename update_ file')

def callMacro(pfile):
    import win32com.client
    from win32com.client import constants as comConst
    print pfile
    folderf,fileName=changeFiles(pfile)
    print os.path.join(rootf,folderf)
    os.chdir(script_path)
    os.chdir(os.path.join(rootf,folderf))
    current_dir=os.getcwd()
    xl=''
    logging.debug('-Trying to run Excel')
    try:
        print 'trying to update'
        logging.debug('--Excel running')
        xl=win32com.client.Dispatch("Excel.Application")
        xl.Visible = False  #  This is for making Excel visible
    except:
        logging.debug('--Cannot run Excel')
        print 'sub:cannot open Excel'+ fileName
    logging.debug('-Trying to run open file')
    try:
        p=os.path.join(current_dir,fileName)
        print 'trying to load file'
        xl.Workbooks.Open(Filename=p,UpdateLinks=False)
        xl.DisplayAlerts = 0
        #xl.Application.CommandBars("Worksheet Menu Bar").Controls("File").Controls("Save As...").Enabled = False
        workbook = xl.ActiveWorkbook
        time.sleep(5)
        logging.debug('--File loaded with success')
    except:
        logging.debug('--Cannot open file')
        print 'cannot open '+ fileName
    logging.debug('-Trying to run macro  ' +str(fileName+"!PT.PT"))
    try:        
        xl.Application.Run(fileName+"!PT.PT")
        #xl.RefreshAll()  #use for refreshing without VBA script
        logging.debug('--running macro finished with success  ')
    except:
        logging.debug('--Cannot run macro')
        print 'cannot run Macro in '+ fileName
    logging.debug('-Trying to save file')
    try:
        workbook.Save()
        workbook.Close()
        logging.debug('--File saved')
      
    except:
        logging.debug('--Cannot save file')
        print 'cannot save '+ fileName
    logging.debug('-Quitting Excel')
    try:
        xl.Application.Quit()
        changeBack(folderf,fileName)
    except:
        logging.warning('--cannot quit excel')
        print 'cannot quit '+ fileName
    del xl


x_=0
while True:
    if prevPID=='root':
        chkpid=False
    else:
        chkpid=check_pid(int(prevPID))
        logging.info("PID check ")
    if chkpid or isExcelRunning():
        print 'PID or excel is not ok, retrying after 60 sec'
        logging.debug("PID or excel is not ok"+str(chkpid)+' '+str(prevPID)+' '+str(isExcelRunning()))
        time.sleep(60)
        x_=x_+1
        if x_>120:
            logging.debug("Update run too long")
            sys.exit()
            
    else:
        print 'pid and Excel is ok , running update ..'
        logging.info('Trying to update file')
        #callMacro(filename)
        try:
            callMacro(filename)
            print 'finished macro'
            logging.info('Excel is updated')
        except:
            logging.debug('Cannot update excel file')
        break
 
print  "===================END=================="
sys.exit()
#pool=ThreadPool(processes=1)
#asy=pool.apply_async(returnPID,(filename,))
#print 'finished waiting updating'+filename
#if !(isExcelRunning()) and !check_pid(prevPID):
#time.sleep(5)
#callMacro(filename)
