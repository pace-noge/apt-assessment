# Courier Service
### Flask application for Courier Service

##### basic requirements:
* Python 3

##### Installation
* Clone this repo using git
```bash
git clone https://github.com/pace-noge/apt-assessment.git
```
* Move to apt-assessment folder
```bash
cd apt-assessment
```
* create new virtual environment:
```bash
pyvenv env
```
* Activate the virtual environment
```bash
source env/bin/activate
```
* Install all requirements needed by this app using pip
```bash
pip install -r requirements.txt
```
* Create new user by running
```bash
python create_admin.py
```
* Run the apps
```bash
python run.py
```

please refer to [python pip](https://docs.python.org/3/tutorial/venv.html) for more reference using pip for installing python lib


### Application Usage:

#### Login

After installation of requirements complete, and you already create user, you can start to use this apps by point your browser to [Courier Service](http://localhost:5000/) the login page will show up. Please enter your credential that you create before.

![alt text](https://raw.githubusercontent.com/pace-noge/apt-assessment/master/docs/login_page.png 'Login Page')

#### Home Screen
![alt text](https://raw.githubusercontent.com/pace-noge/apt-assessment/master/docs/home.png 'home screen')

#### Courier

##### Courier List
access to Courier list can be done by clicking on Courier menu at sidebar, then the courier list page will show
![alt text](https://raw.githubusercontent.com/pace-noge/apt-assessment/master/docs/courier_list.png 'courier list')

#### Create new courier
on Courier list page, click at Add button, then the modal form for creating new courier will pop up
![alt text]( 'New Courier')