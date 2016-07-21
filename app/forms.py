from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms_components import TimeField
from wtforms.validators import DataRequired
from .models import Courier


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class CourierForm(Form):
    name = StringField('name', validators=[DataRequired()])
    address = TextAreaField('address', validators=[DataRequired()])
    available_time_start = StringField('available from', validators=[DataRequired()])
    available_time_stop = StringField('Available until', validators=[DataRequired()])


class DeliveryJobForm(Form):
    pickup_address = StringField(
                        'Pickup Address',
                        validators=[DataRequired()]
                    )
    pickup_address_additional_info = TextAreaField(
                                        'Pickup Address Additional Info'
                                    )
    pickup_date = StringField('Pickup Date', validators=[DataRequired()])
    pickup_time = StringField(
                    'Pickup Time',
                    validators=[DataRequired()]
                )
    drop_off_address = StringField(
                            'Drop Off Address',
                            validators=[DataRequired()]
                        )
    drop_off_additional_info = TextAreaField(
                                    "Drop Off Additional Info"
                                )
    deliver_date = StringField('Deliver Date', validators=[DataRequired()])
    delivered_time = StringField('Delivered Time')
    item = StringField('Item', validators=[DataRequired()])
    courier = SelectField(
                u'Courier',
                choices=[
                    (c.id, c.name) for c in Courier.query.all()
                    ],
                coerce=int
            )
