from app import app, db, lm
from .forms import LoginForm, CourierForm, DeliveryJobForm
from .models import User, Courier, DeliveryJob
from datetime import datetime, time as d_time
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
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
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
    return render_template(
            'courier.html',
            page_title="Couriers",
            couriers=couriers,
            form=form
        )


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
        return render_template(
                    'courier_detail.html',
                    courier=courier,
                    page_title=courier.name,
                    form=form
                )
    else:
        return page_not_found(courier)


@app.route("/couriers/<id>/delete/")
@login_required
def delete_courier(id):
    courier = Courier.query.filter_by(id=id)
    if courier is not None:
        courier.delete()
        db.session.commit()
        return redirect('/couriers/')
    else:
        return page_not_found(courier)


@app.route('/delivery-jobs', methods=['GET', 'POST'])
@app.route('/delivery-jobs/', methods=['GET', 'POST'])
def delivery_jobs():
    jobs = DeliveryJob.query.all()
    form = DeliveryJobForm()
    if form.validate_on_submit():
        pickup_address = form.pickup_address.data
        pickup_address_additional_info = form.pickup_address_additional_info.data
        pickup_time = convert_to_py_datetime(
            form.pickup_date.data,
            form.pickup_time.data
        )
        drop_off_address = form.drop_off_address.data
        drop_off_additional_info = form.drop_off_additional_info.data
        delivered_time = convert_to_py_datetime(
            form.deliver_date.data,
            form.delivered_time.data
        )
        item = form.item.data
        courier = Courier.query.get(form.courier.data)
        d = DeliveryJob(
            pickup_address=pickup_address,
            pickup_address_additional_info=pickup_address_additional_info,
            pickup_time=pickup_time,
            drop_off_address=drop_off_address,
            drop_off_additional_info=drop_off_additional_info,
            delivered_time=delivered_time,
            item=item,
            courier=courier,
            creator=current_user
        )
        db.session.add(d)
        db.session.commit()
        return redirect('/delivery-jobs/')

    else:
        flash_error(form)
    return render_template('delivery_jobs.html', jobs=jobs, form=form)



@app.route('/delivery-jobs/<id>/', methods=["GET", "POST"])
def dj_detail(id):
    d = DeliveryJob.query.get(id)
    form = DeliveryJobForm(obj=d)
    if form.validate_on_submit():
        pickup_address = form.pickup_address.data
        pickup_address_additional_info = form.pickup_address_additional_info.data
        pickup_time = convert_to_py_datetime(
            form.pickup_date.data,
            form.pickup_time.data
        )
        drop_off_address = form.drop_off_address.data
        drop_off_additional_info = form.drop_off_additional_info.data
        delivered_time = convert_to_py_datetime(
            form.deliver_date.data,
            form.delivered_time.data
        )
        print(type(delivered_time))
        item = form.item.data
        courier = Courier.query.get(form.courier.data)

        d.pickup_address=pickup_address
        d.pickup_address_additional_info=pickup_address_additional_info
        d.pickup_time=pickup_time
        d.drop_off_address=drop_off_address
        d.drop_off_additional_info=drop_off_additional_info
        d.delivered_time=delivered_time
        d.item=item
        d.courier=courier
        d.last_modified_by = current_user
        db.session.add(d)
        db.session.commit()
        return redirect('/delivery-jobs/%s/' % d.id)
    else:
        flash_error(form)
    return render_template('delivery_job_detail.html', job=d, form=form)


@app.route('/delivery-jobs/<id>/delete/')
def delete_delivery_jobs(id):
    d = DeliveryJob.query.filter_by(id=id)
    if d is not None:
        d.delete()
        db.commit()
        return redirect('/delivery-jobs/')
    return page_not_found(d)


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
    return render_template('test.html')

def convert_12_to_24(str_time):
    s = time.strptime(str_time, "%I:%M %p")
    return d_time(s.tm_hour, s.tm_min)

def convert_to_py_datetime(str_date, str_time):
    t = convert_12_to_24(str_time)
    d = str_date.split("/")
    return datetime(int(d[2]), int(d[1]), int(d[0]), t.hour, t.minute)