from app import app, db, lm
from .models import User, Courier, Item, DeliveryJob
from flask import render_template



@lm.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')



@app.route('/couriers')
def courier_list():
    return "Courier list Page"

