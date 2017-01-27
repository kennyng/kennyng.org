"""
    config/default.py
    ------------------
    Default configuration settings for Flask app.

"""
import os


DEBUG = os.environ.get('FLASK_DEBUG', True)
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')
USERNAME = os.environ.get('FLASK_USERNAME', 'admin')
SALT = os.environ.get('FLASK_SALT', 'default-password-salt')
PASSWORD = os.environ.get('FLASK_PASSWORD',
                          'pbkdf2:sha1:1000$PyroY8oH$f750609556f5da1bf3a0bb051b82e75fd5c57579')


APP_NAME = os.environ.get('OPENSHIFT_APP_NAME', 'homepage')
HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS', 'localhost')
IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', PROJECT_DIR),
                                       '{}.db'.format(APP_NAME))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DATABASE)
