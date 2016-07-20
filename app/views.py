from app import app, db, lm
from .forms import LoginForm
from .models import User, Courier, Item, DeliveryJob
from flask import render_template, flash, redirect



@lm.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        try:
            user.check_password(form.password.data)
            flash('Login requested for user "%s"' % (form.username.data))
            return redirect('/index')
        except:
            flash("Invalid username or password")
    return render_template('login.html',
        title='Login',
        form=form
    )

@app.route('/couriers')
def courier_list():
    return "Courier list Page"

