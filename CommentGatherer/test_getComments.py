import unittest
import getComments
import os

class Test(unittest.TestCase):
    def test_create_candidate_files_list(self):
        self.assertEqual(getComments.create_candidate_files_list(),['.\\.\\RA_xx_as.xlsx'])
    def test_create_candidate_files_list__no_dir_file(self):
        os.rename('dirs.txt', 'dirs.txt1')
        self.assertEqual(getComments.create_candidate_files_list(),['.\\.\\RA_xx_as.xlsx'])
        os.rename( 'dirs.txt1','dirs.txt')
    def test_DataBase_non_exsting_db_file(self):
        try:
            os.rename('comments.db', 'comments.db1')
        except:
            pass
        db = getComments.DataBase('comments.db')
        db.close()
        os.remove('comments.db')
        try:
            os.rename('comments.db1', 'comments.db')
        except:
            pass
    def test_DataBase_write(self):
        if os.path.exists('comments.db'):
            db = getComments.DataBase('comments.db')
            kwarg = {'insert_date':'2015.07.01',
                     'filename':'file',
                     'cust_type':'cust',
                     'happened':'2015.07.01',
                     'noticed':'2015.07.01',
                     'period':'0',
                     'author':'ja',
                     'desc':'dscriotion',
                     'sheet':'aaa',
                     'row_num':'999',
                     'path':'./sd/',
                     'original_text':'some text',
                     'monthly_flag':'1',
                     'new_flag':'1',
                     'real_flag':'1',
                     'dublicates_flag':'1',
                     'share_flag':'0',
                     'todo_flag':'1',
                     'error_flag':'0'}
            db.write(kwarg)
            db.close()
            
    def test_write_skipped_records_to_file(self):
        getComments.write_skipped_records_to_file('test test')
        
    def test_write_skipped_records_to_file__no_file(self):
        getComments.write_skipped_records_to_file('test test')
        #try:
        #    os.rename('SkippedRecords.csv1','SkippedRecords.csv')
        #except:
        #    pass
    
    def test_open_candidate_files__ok(self):
        getComments.open_candidate_files(['RA_xx_as.xlsx'])
    def test_parse_comment(self):
        self.assertEqual(len(getComments.parse_comment('[2015.07.01 - 2015.06.01 ja] test #m #p')),14)
        self.assertEqual(len(getComments.parse_comment('[2015.07.01 - 2015.06.01 ja] ')),14)
        self.assertEqual(type(getComments.parse_comment(' test #m #p')),type(None))
        self.assertEqual(type(getComments.parse_comment('[2015test - 2015.06.01 ja] test #m #p')),type(None))
        self.assertEqual(len(getComments.parse_comment('[2015.07.01 - 20150601 ] test ')),14)
        self.assertEqual(getComments.parse_comment('[2015.07.01 - 2015.06.01 ja] #m')['monthly_flag'],'1')
        self.assertEqual(getComments.parse_comment('[2015.07.01 - 2015.06.01 ja] #p')['pending_flag'],'1')
        self.assertEqual(getComments.parse_comment('[2015.07.01 - 2015.06.01 ja] #m')['author'],'ja')
        self.assertEqual(getComments.parse_comment('[2015.07.01 - 2015.06.01 ja] #m')['happened'],'2015-07-01')
        self.assertEqual(getComments.parse_comment('[2015.07.01 - 2015.06.01 ja] #m')['noticed'],'2015-06-01')
        self.assertEqual(getComments.parse_comment('[20150701 - 2015.06.01 ja] #m')['happened'],'1970-01-01')
        self.assertEqual(getComments.parse_comment('[2015.07.01 - 2015.06.01 ja] #m')['error_flag'],'1')
    def test_search_alarm_in_columns(self):
        getComments.search_alarm_in_columns('alarm=[y:nl:10] net vs cg (treshold)','filename','sheet1',1)
    def test_send_alarm_emails(self):
        getComments.search_alarm_in_columns('[y:nl:10] net vs cg (treshold)','filename','sheet1',1)
        getComments.search_alarm_in_columns('[y:hr:20] net vs cg (treshold)','filename','sheet1',1)
        getComments.search_alarm_in_columns('[y:nl:10] ne (treshold)','filename','sheet1',1)
        getComments.search_alarm_in_columns('[y:nl:10] cg (treshold)','filename','sheet1',1)
        getComments.search_alarm_in_columns('[y:hr:20] net  (treshold)','filename','sheet1',1)
        #a=getComments.get_alarm_list()
        print getComments.send_alarm_emails()

if __name__ == '__main__':
    unittest.main()
