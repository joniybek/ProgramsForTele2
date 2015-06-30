from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
control_container = Table('control_container', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String(length=500)),
    Column('meta', String(length=140)),
    Column('g_config', String(length=500)),
    Column('user_id', Integer),
    Column('creation_date', DateTime),
    Column('sql_script', String(length=2500)),
    Column('update_time', String(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['control_container'].columns['sql_script'].create()
    post_meta.tables['control_container'].columns['update_time'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['control_container'].columns['sql_script'].drop()
    post_meta.tables['control_container'].columns['update_time'].drop()
