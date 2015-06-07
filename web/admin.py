import os

from flask import redirect, request, session, url_for, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from wtforms import Form, StringField, PasswordField
from wtforms.validators import InputRequired, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import Markup

from web import app, db
from web.models import Book, Project, Post, Tag


def validate_login(form, field):
        if form.username.data != app.config['USERNAME']:
            raise ValidationError('Invalid username or password.')

        pw = (form.password.data + app.config['SALT']).encode('utf_8')
        if not check_password_hash(app.config['PASSWORD'], pw):
            raise ValidationError('Invalid username or password.')

class LoginForm(Form):
    username = StringField('Username', [InputRequired("<Username> field is required.")])
    password = PasswordField('Password', [InputRequired("<Password> field is required."),
                                          validate_login])

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'error')


class AuthIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not session.get('is_authenticated', False):
            return redirect(url_for('.login'))
        return super(AuthIndexView, self).index()

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            session['is_authenticated'] = True
            session['user'] = form.username.data
            flash('You are now logged in. Welcome!', 'success')
            return redirect(url_for('.index'))

        flash_errors(form)
        self._template_args['form'] = form
        return super(AuthIndexView, self).index()

    @expose('/logout/')
    def logout(self):
        session.pop('is_authenticated', None)
        flash('You are now logged out. Goodbye!', 'success')
        return redirect(url_for('.index'))


class AuthModelView(ModelView):
    def is_accessible(self):
        return session.get('is_authenticated', False)

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('admin.login', next=request.url))


class BookView(AuthModelView):
    def _list_format_thumbnail(view, context, model, name):
        if not model.image:
            return ''
        return Markup('<img src="{}" width="185" height="280">'.format(model.image))

    def _list_format_link(view, context, model, name):
        if not getattr(model, name):
            return ''
        return Markup('<a href="{url}" rel="external" target="_blank">{url}</a>'.format(
            url=getattr(model, name)))

    column_formatters = dict(image=_list_format_thumbnail,
                             url=_list_format_link)
    column_labels = dict(image='Cover Image', url='URL')
    column_sortable_list = ('year', 'title')
    column_searchable_list = ('year', 'title')

    form_args = dict(url=dict(label='Book URL'),
                     image=dict(label='Image URL'))


class ProjectView(AuthModelView):
    def _list_format_thumbnail(view, context, model, name):
        if not model.image:
            return ''
        return Markup(('<a href="{url}" target="_blank">'
                       '<img src="{url}" width="180">'
                       '</a>').format(url=model.image))

    def _list_format_links(view, context, model, name):
        project, info, code  = '', '', ''
        if model.url:
            project = model.url
        if model.info:
            info = model.info
        if model.code:
            code = model.code
        return Markup(
                ('<p><strong>PROJECT: </strong>\n'
                 '<a href="{project}" rel="external" target="_blank">{project}</a></p>\n'
                 '<p><strong>ABOUT: </strong>\n'
                 '<a href="{info}" rel="external" target="_blank">{info}</a></p>\n'
                 '<p><strong>CODE: </strong>\n'
                 '<a href="{code}" rel="external" target="_blank">{code}</a></p>\n'
                ).format(project=project, info=info, code=code))

    column_formatters = dict(image=_list_format_thumbnail,
                             url=_list_format_links)
    column_list = ('category', 'title', 'url', 'image')
    column_labels = dict(url='URL(s)')
    column_sortable_list = ('category', 'title')
    column_searchable_list = ('category', 'title')

    form_args = dict(url=dict(label='Project/Demo URL'),
                     paper=dict(label='Info URL'),
                     code=dict(label='Code Repo URL'),
                     image=dict(label='Image URL'))


class PostView(AuthModelView):
    column_display_pk = True
    column_list = ('id', 'title', 'pub_date', 'tags', 'is_published')
    column_labels = dict(id='id', pub_date='Published Date', tags='Tag(s)',
                         is_published='Published?')
    column_sortable_list = ('id', 'title', 'pub_date', 'is_published')
    column_searchable_list = ('id', 'title', 'pub_date')


class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return session.get('is_authenticated', False)

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('admin.login', next=request.url))

    can_upload = False
    can_delete = False
    can_delete_dirs = False
    can_mkdir = False
    can_rename = False


# Create Admin class instance and override defaults
admin = Admin(app, name='Kenny Ng :: Admin',
              index_view=AuthIndexView(),
              base_template='admin/custom_master.html',
              template_mode='bootstrap3')

# Add administrative model views
admin.add_view(BookView(Book, db.session))
admin.add_view(ProjectView(Project, db.session))
admin.add_view(PostView(Post, db.session, name='Blog: Post', endpoint='blog'))
admin.add_view(AuthModelView(Tag, db.session, name='Blog: Tag'))

path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(CustomFileAdmin(path, '/static/', name='Static Assets', endpoint='static-assets'))
