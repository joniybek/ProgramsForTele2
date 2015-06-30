# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
#import numpy as np
import sqlite3 as lite
import os
import csv
import re

# <codecell>

def connectLite():
    conLite = None
    try:
        conLite = lite.connect(os.path.join(basedir, 'data.db'))
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        #.exit(1)
    return conLite

# <codecell>

def readTrend(snum,conLite):
    df=pd.read_sql("select d_timestamp,volume from trend_data where contr_id='"+snum+"' and d_timestamp>date('now','-65 days') order by date(d_timestamp) ",conLite,parse_dates='d_timestamp')
    df.columns = map(str.lower, df.columns)
    df=df.set_index('d_timestamp')
    return df

# <codecell>

def dfToNf(ts):
    a=ts.to_csv(date_format='%Y/%m/%d',quoting = csv.QUOTE_NONNUMERIC,header = False)
    a='['+re.sub(r'(".*")(.*)','[new Date('+ r'\g<1>'+') ' + r'\g<2>'+'],',a)[:-1]+'],'+'{ labels: [ '+'"'+'","'.join(ts.reset_index().columns.values)+'"'+' ]'
    return a       


def getNF(vList):

    #conLite=connectLite()
    conLite = lite.connect(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db'))
    dataframe_list=list()
    #curLite = conLite.cursor()
    #curLite.execute('select contr_id, script from controls where active_flag=1')
    for ci in vList: #curLite.fetchall():
        snum=ci.name
        ts=readTrend(snum, conLite)
        a= dfToNf(ts)
        dataframe_list.append((ci,a))
        #with open("c:\\Output.txt", "w") as text_file:
        #    text_file.write(a)
        #conLite.close()
    return dataframe_list




