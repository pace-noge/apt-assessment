from app import app, db, lm
from .forms import LoginForm, CourierForm
from .models import User, Courier, DeliveryJob
from datetime import time as d_time
import time
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
@login_required
def courier_list():
    form = CourierForm()
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        available_time_start = convert_12_to_24(form.available_time_start.data)
        available_time_stop = convert_12_to_24(form.available_time_stop.data)
        courier = Courier(
            name=name,
            address=address,
            available_time_start=available_time_start,
            available_time_stop=available_time_stop,
            creator=current_user,
            last_modified_by=current_user
        )
        db.session.add(courier)
        db.session.commit()
        return redirect('/couriers/')
    else:
        flash_error(form)

    couriers = Courier.query.all()
    return render_template('courier.html', page_title="Couriers", couriers=couriers, form=form)


@app.route('/couriers/<id>/', methods=['GET', 'POST'])
@login_required
def courier_detail(id):
    courier = Courier.query.get(id)
    if courier is not None:
        form = CourierForm(obj=courier)
        if form.validate_on_submit():
            courier.name = form.name.data
            courier.address = form.address.data
            courier.available_time_start = convert_12_to_24(form.available_time_start.data)
            courier.available_time_stop = convert_12_to_24(form.available_time_stop.data)
            courier.last_modified_by = current_user
            db.session.add(courier)
            db.session.commit()
            return redirect("/couriers/%s/" % courier.id)
        return render_template('courier_detail.html', courier=courier, page_title=courier.name, form=form)
    else:
        return page_not_found(courier)




@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


def flash_error(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                  getattr(form, field).label.text,
                  error
            ))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/lte")
def lte():
    return render_template('base_lte.html')

def convert_12_to_24(str_time):
    s = time.strptime(str_time, "%I:%M %p")
    return d_time(s.tm_hour, s.tm_min)