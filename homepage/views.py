"""
    homepage/views.py
    ---------------
    Defines the routes for the application.

"""
from datetime import date
from flask import (abort, redirect, render_template, request,
                    session, url_for, flash)
from sqlalchemy import exc

from homepage import app, db
from homepage.models import Project, Link, Tag


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/projects', strict_slashes=False)
def projects():
    error = False
    try:
        projects = Project.query.filter_by(visible=True).order_by(Project.date.desc()).all()
    except exc.SQLAlchemyError:
        error = True
        projects = []

    return render_template('projects.html', projects=projects, error=error)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def init_db():
    """Deletes and re-creates database tables."""
    db.drop_all()
    db.create_all()
