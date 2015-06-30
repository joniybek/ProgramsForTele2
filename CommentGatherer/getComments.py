#!/usr/bin/python
import logging
#import pymsgbox
import sys
import os
script_path=os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)
#logging.basicConfig(filename=('getComments.log'),format='%(levelname)s : %(asctime)s %(message)s',level=logging.DEBUG)
#logging.info(' started to run with arguments'+ str(sys.argv))
import glob
import xlrd
import re
from datetime import datetime
from mmap import mmap,ACCESS_READ
from xlrd import open_workbook, cellname
import sys
#filePattern='s*'
today=datetime.now()
todayf=today.strftime("%Y_%m_%d_%H%M")
error_flag=0
rel_root='../../../'
path=os.path.dirname(sys.argv[0])
fileList=[]
finalMsg=''
currentfile=''
sshclient=''
regP1=re.compile('[\[\]]?(\d{2,}[-/\\.\s]{0,3}\d{2,}[-/\\.\s]{0,3}\d{2,})[-/\\.\s]{0,3}(\d{2,}[-/\\.\s]{0,3}\d{2,}[-/\\.\s]{0,3}\d{2,})[-/\\.\s]{0,4}(\w{1,})[\[\]]?\s*(.*)')  
print 'compiled reg'
import sqlite3 as lite
def getCur():
    try:
        con = lite.connect('comments.db')
        cur = con.cursor()
        cur.execute("create table if not exists comment(insert_date TIMESTAMP, filename TEXT, customer_type TEXT, happened TIMESTAMP, noticed TIMESTAMP,period TEXT, author TEXT, description TEXT, sheet_name TEXT, row_num TEXT, path TEXT,original_text TEXT UNIQUE, monthly_flag BOOLEAN,new_flag BOOLEAN,real_flag BOOLEAN, dublicates_flag BOOLEAN,share_flag BOOLEAN,todo_flag BOOLEAN, error_flag BOOLEAN, skip_flag  BOOLEAN)")
        cur.execute('select count(1) from comment')
        print cur.fetchone()
        return con
    except:
        return ''
con=getCur()
def writeToDb(tup1):
    global con
    with con:
        cur = con.cursor()
        for i in tup1:
           try:
                cur.execute("INSERT INTO comment (insert_date,filename,customer_type,happened,noticed,period,author,description,sheet_name,row_num,path,original_text,monthly_flag,new_flag,real_flag,dublicates_flag,share_flag,todo_flag, error_flag) VALUES(?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", i)
                con.commit()
                print "inserted"+'\n'
         except:
                pass
    
def getFiles():
    filePattern='*RA_??_*.xls*'
    fileList=[]
    with open('dirs.txt') as dirs:
        rel_dirs=dirs.readlines()
    dirs.close()
    for i in rel_dirs:
        print os.path.join(rel_root,i.rstrip(),filePattern)
        tmp=glob.glob(os.path.join(rel_root,i.rstrip(),filePattern))
        for jj in tmp:
            fileList.append(jj)
    return fileList


def writeToFile(text):
    f = open('SkippedRecords.csv',"a")
    f.write(text)
    f.close()
def parseData(strn):
    global error_flag
    error_flag=0
    global filename
    monthly_flag=0
    real_flag=0
    dublicates_flag=0
    new_flag=0
    share_flag=0
    todo_flag=0
    pending_flag=0

    def resetData():  #this is for default value when comment doesnt follow pattern, it returns first day of month
        import datetime
        return datetime.datetime(1970, 1, 1) 
    def checkData(matchObjGroup): #this checks weather object group is correct, I should give obj group here, then it will get each num from them
        regp1='(\d{4})[-/\\.\s]{1,3}(\d{2})[-/\\.\s]{1,3}[\s]{0,2}(\d{2})'
        regp2='(\d{2})[-/\\.\s]{1,3}(\d{2})[-/\\.\s]{1,3}[\s]{0,2}(\d{2,})'
        if re.match(regp1,matchObjGroup):
            tmp4=re.match(regp1,matchObjGroup)
            try:
                hapn4=datetime.strptime(str(tmp4.group(1))+str(tmp4.group(2))+str(tmp4.group(3)),'%Y%m%d')
                return hapn4
            except:
                pass
        elif re.match(regp1,matchObjGroup):
            tmp2=re.match(regp1,matchObjGroup)
            try:
                hapn2=datetime.strptime(str(tmp2.group(1))+str(tmp2.group(2))+str(tmp2.group(3)),'%y%m%d')
                return hapn2
            except:
                pass
        else:
            return resetData()
    mobj=regP1.match(strn)
    if mobj:
        happn=checkData(mobj.group(1))
        notic=checkData(mobj.group(2))
        diff=(notic-happn).days
        try:
            diff1=(datetime.now()-happn).days
            diff2=(datetime.now()-notic).days
        except:
            import sys
            print sys.exc_info()
        if diff>20 or diff<0 or diff1>365 or diff2>365 or diff1<0 or diff2<0:
            error_flag=1
        if mobj.group(3):
            init=mobj.group(3)
        else:
            init='N/I'
            error_flag=1
        cmnt=mobj.group(4)
        reghash1=re.compile('(#.)')
        for i in re.findall(reghash1,cmnt):  #add here more hashtags if needed
            if str(i).lower()=='#m':
                monthly_flag=1
            elif  str(i).lower()=='#n':
                new_flag=1
            elif  str(i).lower()=='#r':
                real_flag=1
            elif  str(i).lower()=='#d':
                dublicates_flag=1
            elif  str(i).lower()=='#s':
                share_flag=1
            elif  str(i).lower()=='#t':
                todo_flag=1
            elif  str(i).lower()=='#p':
                pending_flag=1

        return (happn,notic,diff,init,cmnt,str(monthly_flag),str(new_flag),str(real_flag),str(dublicates_flag),str(share_flag),str(todo_flag),str(error_flag),str(pending_flag))
    else:
        writeToFile(str(todayf)+';'+str (strn)+'\n')
		
def createEmail(filename, sheetname, rownum,init,cmnt):
    global finalMsg
    global sshclient
    import paramiko
    from paramiko import SSHClient
    host='***'
    user='***'
    psec='***'
    port=22
    folder='/RAC/scripts/jakhashr/email'
    sshclient = paramiko.SSHClient()
    sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshclient.connect(hostname=host, username=user, password=psec, port=port)
    if '~' not in filename:
        msg_body_tmp= str(init) +': '+cmnt.replace('"', "'")+'   @ ['+filename+' => '+sheetname+' => '+rownum+']  \n'
        finalMsg+=msg_body_tmp
   
def getColComment(sheet,r1,filename,custtype):
    listForOneSheet=[]
    NOW=datetime.now().strftime("%Y-%m-%d %H:%M")
    for i in range(1,sheet.nrows):
        cell_=sheet.cell(i,r1)
        if cell_.value:
            tup=parseData(unicode(cell_.value))  ## here each cell is sent to parse and then returned parsing results
            if tup:
                listForOneSheet.append((NOW,os.path.split(filename)[1],str(custtype),tup[0].strftime("%Y-%m-%d"),tup[1].strftime("%Y-%m-%d"),str(tup[2]),str(tup[3]),str(tup[4]),str(sheet.name),str(i),os.path.split(filename)[0],unicode(cell_.value),tup[5],tup[6],tup[7],tup[8],tup[9],tup[10],tup[11]))
                if tup[12]=='1':
                    try:
                        createEmail(os.path.split(filename)[1],str(sheet.name),str(i),str(tup[3]),str(unicode(cell_.value)))
                    except:
                        print sys.exc_info()
    return listForOneSheet        

def runFiles(list): # this iterates by files
    fileList=list
    global filename
    for filename in fileList:
        try:
            book = xlrd.open_workbook(filename)
            print 'reading   '+str(filename)
        except :
            pass
            print "cannot open file with excel"+str(filename)
        try:
            searchInBook(book,filename)
        except:
            print 'cannot search'
            
def searchInBook(book,filename): #this goes by each sheet object 
    for sheet_index in xrange(book.nsheets):
        sheet=book.sheet_by_index(sheet_index)
        for r1 in range(sheet.ncols):
            try:
                cell1=sheet.cell(0,r1)
                if cell1.ctype==1:
                    tmp=cell1.value
                    if tmp[0:4]=='desc':
                        a=getColComment(sheet, r1,filename,tmp[5:])
                        if a:
                            writeToDb(a)
            except:
                pass
fileList=getFiles()
allComm=[]                        
runFiles(fileList)
if finalMsg: # send messege through mutt client in file server using ssl
    print finalMsg
    msg_cmd_tmp='echo "'+finalMsg+  '"|mutt -s " Pending tasks for '+datetime.now().strftime("%Y-%m-%d")+' " jakhongir.ashrapov@tele2.com '
    stdin, stdout, stderr = sshclient.exec_command(msg_cmd_tmp)
try:
    con.close()
except:
    import sys
    sys.exit(1)

