from app import db
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)


    def is_authenticated(self):
        return self.authenticated


    def is_active(self):
        return self.active


    def is_anonymous(self):
        return False


    def get_id(self):
        return self.id

    def is_admin(self):
        return self.admin

    def __repr__(self):
        return '<User %r>' % (self.username)

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, **kwargs):
        pw_hash = self.set_password(kwargs['password'])
        kwargs['password'] = pw_hash
        print(kwargs)
        super().__init__(**kwargs)


class MetaDataMixin(object):
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @declared_attr
    def creator_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey(
                'user.id',
                name='fk_%s_creator_id' % cls.__name__,
                use_alter=True,
            )
        )

    @declared_attr
    def creator(cls):
        return db.relationship(
            'User',
            primaryjoin='User.id == %s.creator_id' % cls.__name__,
            remote_side='User.id')

    @declared_attr
    def last_modified_by_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey(
                'user.id',
                name='fk_%s_last_modified_by_id' % cls.__name__,
                use_alter=True
            )
        )

    @declared_attr
    def last_modified_by(cls):
        return db.relationship(
            'User',
            primaryjoin='User.id == %s.last_modified_by_id' % cls.__name__,
            remote_side='User.id' )


class Courier(MetaDataMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
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



class DeliveryJob(MetaDataMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courier = db.Column(db.Integer, db.ForeignKey('courier.id'))
    pickup_address = db.column(db.String(120))
    pickup_address_additional_info = db.Column(db.Text)
    drop_off_address = db.Column(db.String(120))
    drop_off_additional_info = db.Column(db.Text)
