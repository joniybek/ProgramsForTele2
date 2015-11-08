from app import db
from app import app
#from app import db2
from app.models import Control_container
import sqlite3 as lite
import os
from models import Refresh_Tasks
#import cx_Oracle
import pandas as pd


def getNF(cname):
    nF='['
    try:
        resultset = db.session.execute("select * from "+ cname +"  order by 1",bind=db.get_engine(app, 'data'))
    except:        
        import sys
        resultset=''
    for r in resultset:
        nF+='[new Date("'+str(r[0])+'"),'+','.join(str(x) for x in list(r)[1:])+'],\n'
    config=Control_container.query.filter_by(name=cname).first()
    if config and str(config.g_config)!='None':
        config=str(config.g_config)
    else:
        if resultset!='':
            config='labels: ["'+'","'.join(resultset.keys())+'"],'
        else:
            config=''
    return nF+'],{'+config 
