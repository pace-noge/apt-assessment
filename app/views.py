from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')



@app.route('/couriers')
def courier_list():
    return "Courier list Page"

