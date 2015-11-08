from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
comment = Table('comment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=500)),
    Column('happened', DateTime),
    Column('noticed', DateTime),
    Column('realf', SmallInteger, default=ColumnDefault(0)),
    Column('monthlyf', SmallInteger),
    Column('newf', SmallInteger),
    Column('freenotef', SmallInteger),
    Column('incidentnum', String(length=20)),
    Column('user_id', Integer),
    Column('report_unit_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comment'].columns['incidentnum'].create()
    post_meta.tables['comment'].columns['monthlyf'].create()
    post_meta.tables['comment'].columns['newf'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comment'].columns['incidentnum'].drop()
    post_meta.tables['comment'].columns['monthlyf'].drop()
    post_meta.tables['comment'].columns['newf'].drop()
