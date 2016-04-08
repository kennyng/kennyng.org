"""
    web/views.py
    ---------------
    Defines the routes for the application.

"""
from datetime import date
from flask import (abort, redirect, render_template, request,
                    session, url_for, flash)
from sqlalchemy import exc

from web import app, db
from web.models import Book, Project, Post, Tag


@app.route('/')
def home():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/resume', strict_slashes=False)
def resume():
    return render_template('resume.html')


@app.route('/projects', strict_slashes=False)
def projects():
    error = False
    try:
        projects = Project.query.order_by(Project.id.desc()).all()
    except exc.SQLAlchemyError:
        error = True
        projects = []

    return render_template('projects.html', projects=projects, error=error)

"""
@app.route('/bookshelf', strict_slashes=False)
def bookshelf():
    error = False
    current_year = date.today().year
    selected = 'CURRENT'

    try:
        books = Book.query.filter_by(
                year=current_year).order_by(Book.id.desc()).all()
    except exc.SQLAlchemyError:
        error = True
        books = []
    filters = get_filters_dict(selected)

    return render_template('bookshelf.html', selected=selected,
                            filters=filters, books=books, error=error)


@app.route('/bookshelf/<option>', methods=['GET'], strict_slashes=False)
def query_books(option):
    error = False
    if option in get_valid_options():
        try:
            if option == 'all':
                selected = 'ALL BOOKS'
                books = Book.query.order_by(Book.id.desc()).all()
            else:
                selected = option
                books = Book.query.filter_by(
                        year=option).order_by(Book.id.desc()).all()
        except exc.SQLAlchemyError:
            error = True
            selected = 'CURRENT'
            books = []
    else:
        abort(404)

    filters = get_filters_dict(selected)
    return render_template('bookshelf.html', selected=selected, filters=filters,
                            books=books, error=error)
"""

@app.route('/notes', methods=['GET'], strict_slashes=False)
def notes():
    error = False
    try:
        tag = request.args.get('tag', None)
        if tag:
            posts = Post.query.filter(Post.tags.any(name=tag)).order_by(Post.pub_date.desc()).all()
        else:
            posts = Post.query.filter_by(is_published=True).order_by(Post.pub_date.desc()).all()
    except exc.SQLAlchemyError:
        error = True
        posts = []

    return render_template('notes_index.html', posts=posts, tag=tag, error=error)


@app.route('/notes/<int:post_id>/<slug>', strict_slashes=False)
def notes_post(post_id, slug):
    try:
        post = Post.query.get_or_404(post_id)
    except exc.SQLAlchemyError:
        abort(404)

    return render_template('notes_post.html', post=post)


#-------------------------------------------------------------------
# HELPER FUNCTIONS
#-------------------------------------------------------------------
def get_valid_options():
    options = ['all']
    current_year = date.today().year
    years = list(reversed(range(2014, current_year)))
    years = list(map(str, years))
    options.extend(years)
    return options


def get_filters_dict(selected):
    filters = []
    current_year = date.today().year
    years = list(reversed(range(2014, current_year)))
    years = map(str, years)
    for year in years:
        if selected != year:
            filters.append({'url': url_for('query_books', option=year),
                            'name': year})
    if selected != 'CURRENT':
        filters[0:0] = [{'url': url_for('bookshelf'), 'name': 'CURRENT'}]
    if selected != 'ALL BOOKS':
        filters.append({'url': url_for('query_books', option='all'),
                        'name': 'ALL BOOKS'})
    return filters

def init_db():
    """Deletes and re-creates database tables."""

    db.drop_all()
    db.create_all()
