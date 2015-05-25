"""
    hello/views.py
    ---------------
    Defines the routes for the application.

"""
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash
from sqlite3 import dbapi2 as sqlite3
from datetime import date
import hashlib
from web import app


#-------------------------------------------------------------------
# DATABASE FUNCTIONS
#-------------------------------------------------------------------
def connect_db():
    """Connects to specified database on request."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Initializes the database."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
        current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def dicts_row(cursor, row):
    """Row factory function that converts each row of results returned from
        the database to dictionaries.
    """
    return dict((cur.description[idx][0], value)
                    for idx, value in enumerate(row))


def query_db(query, args=(), one=False, row_factory=sqlite3.Row):
    """Query helper that combines getting the cursor,
        executing the query, and fetching the results.

    Args:
        query: the query string to execute
        args: arguments to pass to the query string
        one: boolean to return a single result (default: False)
        row_factory: function to convert each row of results
            (default: sqlite3.Row)

    Returns:
        Results from the database in the format of whatever the row factory
        function converts to.
    """
    db = get_db()
    db.row_factory = row_factory
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_db(error):
    """Closes the database at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


#-------------------------------------------------------------------
# ADMIN CONSOLE
#-------------------------------------------------------------------
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))

    try:
        books = query_db('select id, year, title, image, url from books order by id desc')
    except sqlite3.Error:
        books = []
        flash('Unable to query books from the database.', 'error')

    return render_template('admin_index.html', books=books)


@app.route('/admin/sync_book', methods=['POST'])
def sync_book():
    if not session.get('logged_in'):
        abort(401)

    try:
        action = request.form['action']
        if action == '':
            flash('ACTION type required to sync book.', 'error')
            return redirect(url_for('admin'))

        db = get_db()
        key = request.form['id']
        year = request.form['year']
        title = request.form['title']
        image = request.form['image']
        url = request.form['url']

        if action == 'add':
            db.execute('insert into books (year, title, image, url) values (?, ?, ?, ?)',
                        (year, title, image, url))
        elif action == 'update':
            db.execute('update books set year=?, title=?, image=?, url=? where id=?',
                        (year, title, image, url, key))
        elif action == 'delete':
            db.execute('delete from books where id=?', (key,))

        db.commit()
    except sqlite3.Error:
        flash('Unexpected error encountered during sync.', 'error')
        return redirect(url_for('admin'))
    else:
        flash('Book was successfully synced.', 'success')
        return redirect(url_for('admin'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        pw = (request.form['password'] + app.config['SALT']).encode('utf_8')

        if user != app.config['USERNAME']:
            error = 'Invalid username or password.'
        elif hashlib.sha512(pw).hexdigest() != app.config['PASSWORD']:
            error = 'Invalid username or password.'
        else:
            session['logged_in'] = True
            flash('Hello, {}!'.format(app.config['USERNAME']), 'flash')
            return redirect(url_for('admin'))

    return render_template('admin_login.html', error=error)


@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    flash('Goodbye!', 'flash')
    return redirect(url_for('admin_login'))


#------------------------------------------------------------------
# MAIN PAGES
#------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/resume', strict_slashes=False)
def resume():
    return render_template('resume.html')


@app.route('/projects', strict_slashes=False)
def projects():
    return render_template('projects.html')


@app.route('/bookshelf', strict_slashes=False)
def bookshelf():
    error = False
    current_year = date.today().year
    selected = 'CURRENT'

    try:
        books = query_db('select title, image, url from books '
                            'where year=? order by id desc', [current_year])
    except sqlite3.Error:
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
                books = query_db('select title, image, url from books order '
                                    'by id desc')
            else:
                selected = option
                books = query_db('select title, image, url from books '
                                    'where year=? order by id desc', [option])
        except sqlite3.Error:
            error = True
            selected = 'CURRENT'
            books = []
    else:
        abort(404)

    filters = get_filters_dict(selected)
    return render_template('bookshelf.html', selected=selected, filters=filters,
                            books=books, error=error)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


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
