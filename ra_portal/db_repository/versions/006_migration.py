from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
followers = Table('followers', pre_meta,
    Column('follower_id', INTEGER),
    Column('followed_id', INTEGER),
)

post = Table('post', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
)

comment = Table('comment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('report_unit_id', Integer),
)

control_container = Table('control_container', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String(length=500)),
    Column('meta', String(length=140)),
    Column('user_id', Integer),
    Column('creation_date', DateTime),
)

user_view = Table('user_view', post_meta,
    Column('user_id', Integer),
    Column('view_id', Integer),
)

view = Table('view', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String(length=500)),
    Column('meta', String(length=140)),
    Column('user_id', Integer),
    Column('creation_date', DateTime),
)

view_control = Table('view_control', post_meta,
    Column('view_id', Integer),
    Column('control_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['followers'].drop()
    pre_meta.tables['post'].drop()
    post_meta.tables['comment'].create()
    post_meta.tables['control_container'].create()
    post_meta.tables['user_view'].create()
    post_meta.tables['view'].create()
    post_meta.tables['view_control'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['followers'].create()
    pre_meta.tables['post'].create()
    post_meta.tables['comment'].drop()
    post_meta.tables['control_container'].drop()
    post_meta.tables['user_view'].drop()
    post_meta.tables['view'].drop()
    post_meta.tables['view_control'].drop()
