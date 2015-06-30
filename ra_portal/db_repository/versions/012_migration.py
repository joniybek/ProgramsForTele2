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
    Column('freenotef', SMALLINT),
    Column('happened', DATETIME),
    Column('incidentnum', VARCHAR(length=20)),
    Column('monthlyf', SMALLINT),
)

comment = Table('comment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=500)),
    Column('timestamp', DateTime),
    Column('happened', DateTime),
    Column('user_id', Integer),
    Column('report_unit_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['comment'].columns['freenotef'].drop()
    pre_meta.tables['comment'].columns['incidentnum'].drop()
    pre_meta.tables['comment'].columns['monthlyf'].drop()
    post_meta.tables['comment'].columns['timestamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['comment'].columns['freenotef'].create()
    pre_meta.tables['comment'].columns['incidentnum'].create()
    pre_meta.tables['comment'].columns['monthlyf'].create()
    post_meta.tables['comment'].columns['timestamp'].drop()
