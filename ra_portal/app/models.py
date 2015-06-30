from app import db
import datetime
from app import app
from collections import OrderedDict
from hashlib import md5
import flask.ext.whooshalchemy as whooshalchemy

ROLE_USER = 0
ROLE_ADMIN = 1
FALSEF=0


user_view = db.Table('user_view',
    db.Column('id', db.Integer),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('view_id', db.Integer, db.ForeignKey('view.id'))
)
view_control = db.Table('view_control',
    db.Column('id', db.Integer),
    db.Column('view_id', db.Integer, db.ForeignKey('view.id')),
    db.Column('control_id', db.Integer, db.ForeignKey('control_container.id')),
    db.Column('ordering', db.Integer)
)

user_control = db.Table('user_control',
    db.Column('id', db.Integer),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('control_id', db.Integer, db.ForeignKey('control_container.id')),
    db.Column('dtimestamp', db.DateTime),
    db.Column('duration', db.Integer)
)

class Bind(object):
    def __init__(self, bind_key):
        self.bind = db.get_engine(app, bind_key)
    def execute(self, query, params=None):
        return db.session.execute(query, params, bind=self.bind)

class User(db.Model):
    __searchable__ = ['nickname']
    
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    comments = db.relationship('Comment', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    views = db.relationship('View', 
        secondary = user_view, 
        primaryjoin = (user_view.c.user_id == id), 
        secondaryjoin = (user_view.c.view_id == id), 
        backref = db.backref('users', lazy = 'dynamic'), 
        lazy = 'dynamic')
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname

  
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def followed_views(self):
        return View.query.join(user_view,(user_view.c.view_id == View.id)).filter(user_view.c.user_id == self.id).order_by(View.name.desc())
  

    def get_id(self):
        return unicode(self.id)
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def is_following_view(self, view):
        return self.views.filter(user_view.c.view_id == view.id).count() > 0

    def is_following(self, view):
        rs = db.session.execute("select count(*) from user_view where view_id= %s and user_id=%s" % (str(view.id), str(self.id)))
        return rs.fetchone()[0]>0
        

    def follow_view(self, view):
        if not self.is_following(view):
            db.session.execute("insert into user_view (view_id, user_id) values(%s,%s)" % (str(view.id), str(self.id)))
            return self

    def unfollow_view(self, view):
        if self.is_following(view):
            db.session.execute("DELETE FROM user_view where view_id= %s and user_id=%s" % (str(view.id), str(self.id)))
            return self




    def __repr__(self):
        return '<User %r>' % (self.nickname)

whooshalchemy.whoosh_index(app, User)
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text= db.Column(db.String(500))
    happened = db.Column(db.DateTime)
    noticed = db.Column(db.DateTime)
    realf = db.Column(db.SmallInteger, default = FALSEF)
    monthlyf = db.Column(db.SmallInteger, default = FALSEF)
    newf = db.Column(db.SmallInteger, default = FALSEF)
    freenotef = db.Column(db.SmallInteger, default = FALSEF)
    incidentnum=db.Column(db.String(20))
    fileUrl=db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    report_unit_id = db.Column(db.Integer, db.ForeignKey('control_container.id'))

    def __repr__(self):
        return '<Post %r>' % (self.text)
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result



class View(db.Model):
    __searchable__ = ['meta']
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    description = db.Column(db.String(500))
    meta = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime)
    controls = db.relationship('Control_container', 
        secondary = view_control, 
        primaryjoin = (view_control.c.view_id == id), 
        secondaryjoin = (view_control.c.control_id == id), 
        backref = db.backref('views', lazy = 'dynamic'), 
        lazy = 'dynamic')


    def subscribed_controls(self):
        return Control_container.query.join(view_control,(view_control.c.control_id == Control_container.id)).filter(view_control.c.view_id == self.id).order_by(Control_container.name.desc())
 

    def __repr__(self):
        return '<View %r>' % (self.meta)

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result
    
    def is_following_container(self, id):
        rs = db.session.execute("select count(*) from view_control where view_id= %s and control_id=%s" % (str(self.id), str(id)))
        return rs.fetchone()[0]>0
    def follow_container(self,id):
        if not self.is_following_container(id):
            db.session.execute("insert into view_control (view_id, control_id) values(%s,%s)" % (str(self.id), str(id)))
            return self
    def unfollow_container(self, id):
        if self.is_following_container(id):
            db.session.execute("DELETE FROM view_control where view_id= %s and control_id=%s" % (str(self.id), str(id)))
            return self
        
        



class Control_container(db.Model):
    __searchable__ = ['meta']
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    description = db.Column(db.String(500))
    meta = db.Column(db.String(140))
    g_config = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime)
    sql_script = db.Column(db.String(2500))
    update_time = db.Column(db.String(20))
    comments = db.relationship('Comment', backref = 'comment', lazy = 'dynamic')

    @staticmethod
    def make_unique_name(name):
        if Control_container.query.filter_by(name = name).first() == None:
            return name
        version = 2
        while True:
            new_name = name + str(version)
            if Control_container.query.filter_by(name = new_name).first() == None:
                break
            version += 1
        return new_name

    def __repr__(self):
        return '<Control_container %r>' % (self.meta)
whooshalchemy.whoosh_index(app, Control_container)

class Refresh_Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    control_name = db.Column(db.String(64))
    status = db.Column(db.String(10))
    start_at = db.Column(db.String(64))

