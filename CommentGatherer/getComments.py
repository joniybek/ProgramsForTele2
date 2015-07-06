#!/usr/bin/python
import logging
import sys
import os
import glob
import xlrd
import re
from datetime import datetime
import sqlite3 as lite
import collections
import paramiko




# script opeerates in shared network disk, thus change dir
script_path=os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)

logging.basicConfig(filename=('getComments.log'),format='%(levelname)s : %(asctime)s %(message)s',level=logging.INFO)
logging.info(' started to run with arguments'+ str(sys.argv))


today=datetime.now().strftime("%Y_%m_%d_%H%M")
rel_root = '.' #'../../../'
alarm_list = []
pending_msg=''
host='***'
user='***'
psec='***'
port=22
CANDIDATE_FILE_PATTERN = '*RA_??_*.xls*'
DIRS_FILE = 'dirs.txt'
DB_FILENAME = 'comments.db'
SKIPPED_RECORDS_FILE = 'SkippedRecords.csv'
regex_pattern_all=re.compile('[\[\]]?(\d{2,}[-/\\.\s]{0,3}\d{2,}[-/\\.\s]{0,3}\d{2,})[-/\\.\s]{0,3}(\d{2,}[-/\\.\s]{0,3}\d{2,}[-/\\.\s]{0,3}\d{2,})[-/\\.\s]{0,4}(\w{1,})[\[\]]?\s*(.*)')
mailing_groups = {'00':'jakhongir.ashrapov@tele2.com',
                  '10':'jakhongir.ashrapov@tele2.com',
                  '20':'jonni.bek@gmail.com'}

class DataBase(object):
    def __init__(self,DB_FILENAME):
        try:
            if not os.path.exists(DB_FILENAME):
                logging.warning('SQLite db  file not found, creating new one')
            self.con = lite.connect(DB_FILENAME)
            self.cur = self.con.cursor()
            self.cur.execute("create table if not exists comment(insert_date TIMESTAMP,\
            filename TEXT,\
            customer_type TEXT,\
             happened TIMESTAMP, \
             noticed TIMESTAMP,\
             period TEXT, \
             author TEXT, \
             description TEXT, \
             sheet_name TEXT,\
              row_num TEXT, \
              path TEXT,\
              original_text TEXT UNIQUE,\
              monthly_flag BOOLEAN,\
              new_flag BOOLEAN,\
              real_flag BOOLEAN, \
              dublicates_flag BOOLEAN,\
              share_flag BOOLEAN,\
              todo_flag BOOLEAN, \
              error_flag BOOLEAN, \
              skip_flag  BOOLEAN)")
        except:
            self.con=None
            logging.critical('Cannot connect to DB, changes will not be saved in DB')
    def write_all(self,kwargs_list):
        if kwargs_list:
            for kwargs in kwargs_list:
                self.write(kwargs)
    def write(self,kwargs):
        with self.con:
            self.con.cursor()
            try:
                self.cur.execute("INSERT INTO comment(\
                             insert_date,\
                             filename,\
                             customer_type,\
                             happened,noticed, \
                             period,\
                             author,\
                             description,\
                             sheet_name,\
                             row_num,\
                             path,\
                             original_text,\
                             monthly_flag,\
                             new_flag, \
                             real_flag,\
                             dublicates_flag,\
                             share_flag,\
                             todo_flag, \
                             error_flag)\
                             VALUES(?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            [kwargs['insert_date'],
                            kwargs['filename'],
                            kwargs['cust_type'],
                            kwargs['happened'],
                            kwargs['noticed'],
                            kwargs['period'],
                            kwargs['author'],
                            kwargs['desc'],
                            kwargs['sheet'],
                            kwargs['row_num'],
                            kwargs['path'],
                            kwargs['original_text'],
                            kwargs['monthly_flag'],
                            kwargs['new_flag'],
                            kwargs['real_flag'],
                            kwargs['dublicates_flag'],
                            kwargs['share_flag'],
                            kwargs['todo_flag'],
                            kwargs['error_flag']])
                print 'inserted'
            except lite.IntegrityError:
                pass #records which have not changed will not be inserted and cause integrity exception
            except Exception,e:
                print str(e)
                logging.warning('Cannot insert data into DB')
                print 'cannot insert'
    def close(self):
        self.con.close()

def create_candidate_files_list():
    file_list=[]
    try:
        with open(DIRS_FILE) as dirs:
            rel_dirs=dirs.readlines()
    except:
        logging.warning('Cannot read dirs.txt')
        rel_dirs='.'

    for dir in rel_dirs:
        existing_files = glob.glob(os.path.join(rel_root,dir.rstrip(),CANDIDATE_FILE_PATTERN))
        file_list = [file for file in existing_files if '~' not in file]
    return file_list

def write_skipped_records_to_file(text):
    with open(SKIPPED_RECORDS_FILE,"a") as file:
        file.write(text)
"""
class Workbook(object):

    def __init__(self,path_to_file):
        try:
            self.book = xlrd.open_workbook(path_to_file)
            self.filename = path_to_file
            self.current_row_index = 0
            self.current_sheet_index = 0
            self.current_cell = 0
            print 'Reading...   '+str(path_to_file)
            logging.info('Reading ...'+str(path_to_file))
        except Exception,e:
            book = None
            print str(e)
            logging.warning('Cannot open file: '+str(path_to_file))
            return None

    def next_first_cell(self):
        if self.book:
            try:
                print self.current_sheet_index
                for sheet_index in range(self.current_sheet_index,self.book.nsheets):
                    self.current_sheet=self.book.sheet_by_index(sheet_index)
                    self.current_sheet_index = sheet_index
                    try:
                        for row1 in range(self.current_sheet.ncols):
                            self.current_row_index = row1
                            try:
                                cell1=self.current_sheet.cell(0,self.current_row_index)
                                if cell1.ctype==1 and cell1.value!='' and cell1 != self.current_cell:
                                    self.current_cell = cell1
                                    return self.current_cell.value
                            except:
                                print "Cannot get first cell value"
                                pass
                    except:
                        print "Cannot interate over column"
                        pass
            except:
                print "Cannot iterate over sheet"

    def get_filename(self):
        return self.filename
    def set_cust_type(self,cust_type):
        self.cust_type = cust_type
    def set_cust_type(self):
        return self.cust_type
    def get_current_first_cell(self):
        return self.current_first_cell

"""


def open_candidate_files(file_list): # this iterates by files
    db = DataBase(DB_FILENAME)
    for filename in file_list:
        try:
            book = xlrd.open_workbook(filename)
            print 'Reading...   '+str(filename)
            logging.info('Reading ...'+str(filename))
        except Exception,e:
            print str(e)
            return None
            logging.warning('Cannot open file: '+str(filename))
        search_columns_in_workbook(book,filename,db)
    db.close()

def search_columns_in_workbook(book,filename,db): #this goes by each sheet object
    for sheet_index in xrange(book.nsheets):
        sheet=book.sheet_by_index(sheet_index)
        for row1 in range(sheet.ncols):
            try:
                cell1=sheet.cell(0,row1)
                if cell1.ctype==1 and cell1.value!='':
                    first_cell=cell1.value
                    if first_cell[0:4]=='desc':
                        comments_in_sheet = search_comments_in_column(sheet, row1,filename,first_cell[5:])
                        db.write_all(comments_in_sheet)
                    elif first_cell[0:5]=='alarm':
                        search_alarm_in_columns(first_cell[6:],os.path.split(filename)[1],str(sheet.name),row1)
            except:
                pass

def search_alarm_in_columns(alarm_str,filename,sheet_name,row1):
    global alarm_list
    def colname(colx):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if colx <= 25:
            return alphabet[colx]
        else:
            xdiv26, xmod26 = divmod(colx, 26)
            return alphabet[xdiv26 - 1] + alphabet[xmod26]
    alarm = {'status': alarm_str[1],
            'country': alarm_str[3:5],
            'mailing_group': alarm_str[6:8],
            'text': alarm_str[9:],
            'filename':filename,
            'sheet_name':sheet_name,
            'row':colname(row1)   }

    if alarm['status']=='y':
        alarm_list.append(alarm)

def search_comments_in_column(sheet,row,filename,cust_type):
    comments_in_sheet=[]
    now=datetime.now().strftime("%Y-%m-%d %H:%M")
    try: # this needed for continuing to search other cells in case they contain references to pictures
        for i in range(1,sheet.nrows):
            cell_=sheet.cell(i,row)
            if cell_.value:
                #print cell_.value
                try:
                    parsed_dict=parse_comment(unicode(cell_.value))  ## here each cell is sent to parse and then returned parsing results
                except:
                    sys.exc_info()
                if parsed_dict:
                    parsed_dict.update({'insert_date':now,
                                        'filename':os.path.split(filename)[1],
                                        'cust_type':str(cust_type),
                                        'sheet':str(sheet.name),
                                        'path':os.path.split(filename)[0],
                                        'row_num':str(i)}  )
                    comments_in_sheet.append(parsed_dict)

                    if parsed_dict['pending_flag']=='1':
                        try:
                            create_pending_email(os.path.split(filename)[1],str(sheet.name),str(i),str(parsed_dict['author']),str(unicode(cell_.value)))
                        except:
                            print sys.exc_info()
    except:
        pass
    return comments_in_sheet

def parse_comment(strn):
    error_flag=0
    monthly_flag=0
    real_flag=0
    dublicates_flag=0
    new_flag=0
    share_flag=0
    todo_flag=0
    pending_flag=0

    def set_default_date():  #this is for default value when comment doesnt follow pattern, it returns first day of month
        return datetime(1970, 1, 1)
    
    def parse_date(match_group): #this checks weather object group is correct, I should give obj group here, then it will get each num from them
        regex_pattern_date_4d='(\d{4})[-/\\.\s]{1,3}(\d{2})[-/\\.\s]{1,3}[\s]{0,2}(\d{2})'
        regex_pattern_date_2d='(\d{4})[-/\\.\s]{1,3}(\d{2})[-/\\.\s]{1,3}[\s]{0,2}(\d{2})'
        if re.match(regex_pattern_date_4d,match_group):
            tmp4=re.match(regex_pattern_date_4d,match_group)
            try:
                hapn4=datetime.strptime(str(tmp4.group(1))+str(tmp4.group(2))+str(tmp4.group(3)),'%Y%m%d')
                return hapn4
            except:
                pass
        elif re.match(regex_pattern_date_2d,match_group):
            tmp2=re.match(regex_pattern_date_2d,match_group)
            try:
                hapn2=datetime.strptime(str(tmp2.group(1))+str(tmp2.group(2))+str(tmp2.group(3)),'%y%m%d')
                return hapn2
            except:
                pass
        else:
            return set_default_date()

    match_group_all=regex_pattern_all.match(strn)
    if match_group_all:
        happn = parse_date(match_group_all.group(1)) #parse dates
        notic = parse_date(match_group_all.group(2))
        diff=(notic-happn).days
        try:                                
            diff1=(datetime.now()-happn).days   #check weather parsed dates logically possible
            diff2=(datetime.now()-notic).days
        except:
            print sys.exc_info()
        if diff>20 or diff<0 or diff1>365 or diff2>365 or diff1<0 or diff2<0:
            error_flag=1
        if match_group_all.group(3):
            init=match_group_all.group(3)
        else:
            init='N/I'
            error_flag=1
        comment_body=match_group_all.group(4)
        regex_hashtag=re.compile('(#.)')
        for i in re.findall(regex_hashtag,comment_body):  #add here more hashtags if needed
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

        return {'happened':happn.strftime("%Y-%m-%d"),
                'noticed':notic.strftime("%Y-%m-%d"),
                'period':str(diff),
                'author':str(init),
                'desc':str(comment_body),
                'monthly_flag':str(monthly_flag),
                'new_flag':str(new_flag),
                'real_flag':str(real_flag),
                'dublicates_flag':str(dublicates_flag),
                'share_flag':str(share_flag),
                'todo_flag':str(todo_flag),
                'error_flag':str(error_flag),
                'pending_flag':str(pending_flag),
                'original_text':strn       }
    else:
        write_skipped_records_to_file(str(datetime.now().strftime("%Y-%m-%d %H:%M"))+';'+str (strn)+'\n')

def create_pending_email(filename, sheetname, rownum,init,comment_body):
    global pending_msg
    pending_msg+= str(init) +': '+comment_body.replace('"', "'")+'   @ ['+filename+' => '+sheetname+' => '+rownum+']  \n'

def send_pending_email():
    global pending_msg
    if pending_msg:
        send_email(pending_msg,mailing_groups['00'],'Pending tasks for:')

def send_alarm_emails():
    global alarm_list
    if len(alarm_list)==0:
        return  None
    groups = collections.defaultdict(list)
    for d in alarm_list:
        groups[d['mailing_group']].append(d)
    email_groups = groups.values()
    #return email_groups
    for group in email_groups:
        msg = ''
        for email in group:
            msg += str(email['country'])+' : '+str(email['text'])+' =>'+str(email['filename'])+'=>'+str(email['sheet_name'])+'=>'+str(email['row']+'\n')
        send_email(msg,mailing_groups[email['mailing_group']], 'Alarms for ')

def send_email(msg,to, title):
    msg_cmd='echo "'+msg+  '"|mutt -s "'+title+datetime.now().strftime("%Y-%m-%d")+' "'+to
    print msg_cmd
    try:
        stdin, stdout, stderr = ssh_client.exec_command(msg_cmd)
        if stderr!='':
            logging.warning('Cannot execute send mail in remote machine :'+stderr)
    except:
        logging.warning('Cannot execute send mail command in this machine')


if __name__ == '__main__':

    open_candidate_files(create_candidate_files_list())
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=user, password=psec, port=port)
    send_pending_email()
    send_alarm_emails()
