from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
courier = Table('courier', pre_meta,
    Column('created', DATETIME),
    Column('updated', DATETIME),
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('name', VARCHAR(length=64)),
    Column('address', TEXT),
    Column('available_time_start', TIME),
    Column('available_time_stop', TIME),
    Column('creator_id', INTEGER),
    Column('last_modified_by_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['courier'].columns['user_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['courier'].columns['user_id'].create()
