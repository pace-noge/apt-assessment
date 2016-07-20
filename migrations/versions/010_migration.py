from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
delivery_job = Table('delivery_job', pre_meta,
    Column('created', DATETIME),
    Column('updated', DATETIME),
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('courier', INTEGER),
    Column('pickup_address_additional_info', TEXT),
    Column('drop_off_address', VARCHAR(length=120)),
    Column('drop_off_additional_info', TEXT),
    Column('creator', INTEGER),
    Column('last_modified_by', INTEGER),
)

delivery_job = Table('delivery_job', post_meta,
    Column('created', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x1007e6550; now>)),
    Column('updated', DateTime, onupdate=ColumnDefault(<sqlalchemy.sql.functions.now at 0x102bcb358; now>), default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x102bcb278; now>)),
    Column('id', Integer, primary_key=True, nullable=False),
    Column('courier', Integer),
    Column('pickup_address_additional_info', Text),
    Column('drop_off_address', String(length=120)),
    Column('drop_off_additional_info', Text),
    Column('creator_id', Integer),
    Column('last_modified_by_id', Integer),
)

courier = Table('courier', pre_meta,
    Column('created', DATETIME),
    Column('updated', DATETIME),
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('name', VARCHAR(length=64)),
    Column('address', TEXT),
    Column('available_time_start', TIME),
    Column('available_time_stop', TIME),
    Column('creator', INTEGER),
    Column('last_modified_by', INTEGER),
)

courier = Table('courier', post_meta,
    Column('created', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x1007e6550; now>)),
    Column('updated', DateTime, onupdate=ColumnDefault(<sqlalchemy.sql.functions.now at 0x102bcb358; now>), default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x102bcb278; now>)),
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('name', String(length=64)),
    Column('address', Text),
    Column('available_time_start', Time),
    Column('available_time_stop', Time),
    Column('creator_id', Integer),
    Column('last_modified_by_id', Integer),
)

item = Table('item', pre_meta,
    Column('created', DATETIME),
    Column('updated', DATETIME),
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR),
    Column('item_type', VARCHAR),
    Column('weight', INTEGER),
    Column('width', INTEGER),
    Column('length', INTEGER),
    Column('height', INTEGER),
    Column('creator', INTEGER),
    Column('last_modified_by', INTEGER),
)

item = Table('item', post_meta,
    Column('created', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x1007e6550; now>)),
    Column('updated', DateTime, onupdate=ColumnDefault(<sqlalchemy.sql.functions.now at 0x102bcb358; now>), default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x102bcb278; now>)),
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('item_type', String),
    Column('weight', Integer),
    Column('width', Integer),
    Column('length', Integer),
    Column('height', Integer),
    Column('creator_id', Integer),
    Column('last_modified_by_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['delivery_job'].columns['creator'].drop()
    pre_meta.tables['delivery_job'].columns['last_modified_by'].drop()
    post_meta.tables['delivery_job'].columns['creator_id'].create()
    post_meta.tables['delivery_job'].columns['last_modified_by_id'].create()
    pre_meta.tables['courier'].columns['creator'].drop()
    pre_meta.tables['courier'].columns['last_modified_by'].drop()
    post_meta.tables['courier'].columns['creator_id'].create()
    post_meta.tables['courier'].columns['last_modified_by_id'].create()
    pre_meta.tables['item'].columns['creator'].drop()
    pre_meta.tables['item'].columns['last_modified_by'].drop()
    post_meta.tables['item'].columns['creator_id'].create()
    post_meta.tables['item'].columns['last_modified_by_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['delivery_job'].columns['creator'].create()
    pre_meta.tables['delivery_job'].columns['last_modified_by'].create()
    post_meta.tables['delivery_job'].columns['creator_id'].drop()
    post_meta.tables['delivery_job'].columns['last_modified_by_id'].drop()
    pre_meta.tables['courier'].columns['creator'].create()
    pre_meta.tables['courier'].columns['last_modified_by'].create()
    post_meta.tables['courier'].columns['creator_id'].drop()
    post_meta.tables['courier'].columns['last_modified_by_id'].drop()
    pre_meta.tables['item'].columns['creator'].create()
    pre_meta.tables['item'].columns['last_modified_by'].create()
    post_meta.tables['item'].columns['creator_id'].drop()
    post_meta.tables['item'].columns['last_modified_by_id'].drop()
