from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
comment = Table('comment', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('report_unit_id', INTEGER),
    Column('text', VARCHAR(length=500)),
    Column('happened', DATETIME),
    Column('timestamp', DATETIME),
    Column('realf', SMALLINT),
)

comment = Table('comment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=500)),
    Column('happened', DateTime),
    Column('noticed', DateTime),
    Column('user_id', Integer),
    Column('report_unit_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['comment'].columns['realf'].drop()
    pre_meta.tables['comment'].columns['timestamp'].drop()
    post_meta.tables['comment'].columns['noticed'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['comment'].columns['realf'].create()
    pre_meta.tables['comment'].columns['timestamp'].create()
    post_meta.tables['comment'].columns['noticed'].drop()
