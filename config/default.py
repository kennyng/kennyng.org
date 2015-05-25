"""
    config/default.py
    ------------------
    Default configuration settings for Flask app.

"""
import os


DEBUG = os.environ.get('DEBUG', False)
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
USERNAME = os.environ.get('USERNAME', 'admin')
SALT = os.environ.get('SALT', 'default-pw-salt')
PASSWORD = os.environ.get('PASSWORD', ('b4563969e043617b2a966764bbcaee0e1a62'
                                      '4646629d075c6aa29a7c7104357054beba86'
                                      '9c71cb4d5f55ebadc13849a4521f8d0a3b2a'
                                      'f4d9723a51b3ccaceb08'))

DATABASE = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', '/tmp'), 'sqlite3.db')
HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS', 'localhost')
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME', 'web')
IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
