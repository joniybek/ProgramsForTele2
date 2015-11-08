import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir, UPLOAD_FOLDER
import sqlite3 as lite

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
db2= lite.connect(os.path.join(basedir, 'data.db'))
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views, models

