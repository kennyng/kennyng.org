"""
    hello/__init__.py
    ------------------
    Initializes Flask application and brings all components together.

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_misaka import Misaka

# Create application object
app = Flask(__name__, instance_relative_config=True,
            static_url_path='/static', static_folder='staticfiles')

# Load default configuration settings
app.config.from_object('config.default')

# Load non-VC configuration variables from instance folder
app.config.from_pyfile('instance.cfg', silent=True)

# Load settings specified by APP_CONFIG_FILE environment variable
#   (such as 'config.development' or 'config.production')
# Variables defined here will override default configurations
#app.config.from_envvar('APP_CONFIG_FILE', silent=True)

# Disable Flask-SQLAlchemy event notification system.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Explicitly add debugger middleware
if app.debug:
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

# Create SQLAlchemy object (database)
db = SQLAlchemy(app)

# Use Misaka for markdown templates
Misaka(app)

# Import main views module (main pages)
from homepage import views
# Import admin views
from homepage import admin
