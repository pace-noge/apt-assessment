from app import db
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.column(db.String)
    is_active = db.Column(db.Boolean)
    authenticated = db.Column(db.Boolean, default=False)
    items = db.relationship('Item', backref='items', lazy='dynamic')
    delivery_jobs = db.relationship('DeliveryJob', backref='delivery_jobs', lazy='dynamic')

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    @property
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class MetaDataMixin(object):
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @declared_attr
    def creator_id(cls):
        return db.Column('creator', db.ForeignKey('user.id'))

    @declared_attr
    def last_modified_by_id(cls):
        return db.Column('last_modified_by', db.ForeignKey('user.id'))

    @declared_attr
    def user(cls):
        return db.relationship("User")


class Courier(MetaDataMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(64), index=True)
    address = db.Column(db.Text)
    available_time_start = db.Column(db.Time)
    available_time_stop = db.Column(db.Time)

    def __repr__(self):
        return '<Courier %r>' % (self.name)


class Item(MetaDataMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    item_type = db.Column(db.String)
    weight = db.Column(db.Integer)
    width = db.Column(db.Integer)
    length = db.Column(db.Integer)
    height = db.Column(db.Integer)
    creator = db.relationship('User', foreign_keys='Item.creator_id')
    last_modified_by = db.relationship(
        'User',
        foreign_keys='Item.last_modified_by_id'
    )



class DeliveryJob(MetaDataMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courier = db.Column(db.Integer, db.ForeignKey('courier.id'))
    pickup_address = db.column(db.String(120))
    pickup_address_additional_info = db.Column(db.Text)
    drop_off_address = db.Column(db.String(120))
    drop_off_additional_info = db.Column(db.Text)
    creator = db.relationship('User', foreign_keys='Item.creator_id')
    last_modified_by = db.relationship(
        'User',
        foreign_keys='Item.last_modified_by_id'
    )
