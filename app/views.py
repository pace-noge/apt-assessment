from app import app, db, lm
from .forms import LoginForm, CourierForm
from .models import User, Courier, Item, DeliveryJob
from flask import render_template, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required



@lm.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        try:
            if user.check_password(form.password.data):
                login_user(user)
                flash('Login requested for user "%s"' % (form.username.data))
                return redirect('/index')
        except:
            flash("Invalid username or password")
    return render_template('login.html',
        title='Login',
        form=form
    )

@app.route('/couriers', methods=['GET', 'POST'])
@app.route('/couriers/', methods=['GET', 'POST'])
def courier_list():
    form = CourierForm()
    if form.validate_on_submit():
        pass
    couriers = Courier.query.all()
    return render_template('courier.html', page_title="Couriers", couriers=couriers, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')