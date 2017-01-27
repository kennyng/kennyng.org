#!/usr/bin/env python
"""
    wsgi.py
    --------
    Entry point for WSGI server.

"""
import os
import sys
import importlib


# Activate virtual environment.
try:
    virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR', '.'), 'virtenv')
    python_version = 'python' + str(sys.version_info[0]) + '.' + str(sys.version_info[1])
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib', python_version, 'site-packages')
    virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
    exec(open(virtualenv).read(), dict(__file___=virtualenv))
except IOError:
    pass

# Provide application to be served by server.
from homepage import app as application


# For testing only (run application locally).
if __name__ == '__main__':
    port = application.config['PORT']
    ip = application.config['IP']
    appname = application.config['APP_NAME']
    hostname = application.config['HOST_NAME']

    framework = "wsgiref"
    try:
        module = importlib.find_loader('flask')
        if module:
            framework = "flask"
    except ImportError:
        pass

    print('STARTING [{}] WSGI SERVER...'.format(framework))
    if application.config['DEBUG']:
        print("="*30 + " DEBUG INFO " + "="*30)
        print("USERNAME: {}".format(application.config['USERNAME']))
        print("APPNAME: {}".format(appname))
        print("HOSTNAME: {} | IP: {} | PORT: {}".format(hostname, ip, port))
        print("PROJECT_DIR: {}".format(application.config['PROJECT_DIR']))
        print("DATABASE_URI: {}".format(application.config['SQLALCHEMY_DATABASE_URI']))
        print("="*72)

    if framework == "flask":
        from flask import Flask
        server = Flask(__name__)
        server.wsgi_app = application
        server.run(host=ip, port=port)
    else:
        from wsgiref.simple_server import make_server
        httpd = make_server(ip, port, application)
        httpd.server_forever()
