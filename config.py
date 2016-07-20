import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'courier.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'migrations')
SQLALCHEMY_TRACK_MODIFICATIONS = True