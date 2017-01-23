"""
    config/default.py
    ------------------
    Default configuration settings for Flask app.

"""
import os


DEBUG = os.environ.get('FLASK_DEBUG', False)
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')
USERNAME = os.environ.get('FLASK_USERNAME', 'admin')
SALT = os.environ.get('FLASK_SALT', 'default-pw-salt')
PASSWORD = os.environ.get('FLASK_PASSWORD', ('pbkdf2:sha1:1000$6b0JlqVL$2779dc6'
                                             '5e4ac3dcc016b6ffdd97cb69a431ca6c7'))

HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS', 'localhost')
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME', 'homepage')
IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', PROJECT_DIR),
                                       '{}.db'.format(APP_NAME))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DATABASE)
