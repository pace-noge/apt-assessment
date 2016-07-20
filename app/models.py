from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.column(db.String)
    is_active = db.Column(db.Boolean)
    authenticated = db.Column(db.Boolean, default=False)

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class ModelBase(db.Model):

    __abstract__ = True

    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class Courier(ModelBase):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(64), index=True)
    address = db.Column(db.Text)
    available_time_start = db.Column(db.Time)
    available_time_stop = db.Column(db.Time)

    def __repr__(self):
        return '<Courier %r>' % (self.name)


class Item(ModelBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    item_type = db.Column(db.String)
    weight = db.Column(db.Integer)
    width = db.Column(db.Integer)
    length = db.Column(db.Integer)
    height = db.Column(db.Integer)


class DeliveryJob(ModelBase):
    id = db.Column(db.Integer, primary_key=True)
    courier = db.Column(db.Integer, db.ForeignKey('courier.id'))
    pickup_address = db.column(db.String(120))
    pickup_address_additional_info = db.Column(db.Text)
    drop_off_address = db.Column(db.String(120))
    drop_off_additional_info = db.Column(db.Text)


    def __repr__(self):
        return '<DeliveryJob %r %r %r>' % (self.courier.name, self.)

