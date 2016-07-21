from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
delivery_job = Table('delivery_job', post_meta,
    Column('created', DateTime, default=ColumnDefault(func.now())),
    Column('updated', DateTime, onupdate=ColumnDefault(func.now()), default=ColumnDefault(func.now())),
    Column('id', Integer, primary_key=True, nullable=False),
    Column('pickup_address', String(length=120)),
    Column('pickup_address_additional_info', Text),
    Column('pickup_time', DateTime),
    Column('drop_off_address', String(length=120)),
    Column('drop_off_additional_info', Text),
    Column('delivered_time', DateTime),
    Column('item', Text),
    Column('courier_id', Integer),
    Column('creator_id', Integer),
    Column('last_modified_by_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['delivery_job'].columns['pickup_address'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['delivery_job'].columns['pickup_address'].drop()
