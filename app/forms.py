from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms_components import TimeField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class CourierForm(Form):
    name = StringField('name', validators=[DataRequired()])
    address = TextAreaField('address', validators=[DataRequired()])
    available_time_start = StringField('available from', validators=[DataRequired()])
    available_time_stop = StringField('Available until', validators=[DataRequired()])