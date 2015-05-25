"""
    hello/__init__.py
    ------------------
    Initializes Flask application and brings all components together.

"""
from flask import Flask


# Create application object
app = Flask(__name__, instance_relative_config=True)

# Load default configuration settings
app.config.from_object('config.default')

# Load non-VC configuration variables from instance folder
app.config.from_pyfile('instance.cfg', silent=True)

# Load settings specified by APP_CONFIG_FILE environment variable
# Variables defined here will override default configurations
# app.config.from_envvar('APP_CONFIG_FILE', silent=True)

# Explicitly add debugger middleware
if app.debug:
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)


# Import views module (decorator functions)
import web.views
