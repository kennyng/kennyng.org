import os

from flask import redirect, request, session, url_for, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from wtforms import Form, StringField, PasswordField
from wtforms.validators import InputRequired, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import Markup

from homepage import app, db
from homepage.models import Project, Link, Tag


def validate_login(form, field):
        if form.username.data != app.config['USERNAME']:
            raise ValidationError('Invalid username or password.')

        pw = (form.password.data + app.config['SALT']).encode('utf_8')
        if not check_password_hash(app.config['PASSWORD'], pw):
            raise ValidationError('Invalid username or password.')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'error')


class LoginForm(Form):
    username = StringField('Username', [InputRequired("<Username> field is required.")])
    password = PasswordField('Password', [InputRequired("<Password> field is required."),
                                          validate_login])


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


class ProjectView(AuthModelView):
    def _list_format_links(view, context, model, name):
        html = ('<a href="{url}" rel="external" target="_blank">{url}</a>'
                ).format(url=model.url)

        if len(model.links) > 0:
            html += '<h6>Additional: </h6>'
        for link in model.links:
            url_str = '<a href="{url}" rel="external" target="_blank">{url}</a><br>'.format(url=link.url)
            html += url_str

        return Markup(html)

    def _list_format_date(view, context, model, name):
        return model.date.strftime('%Y-%m')

    column_display_pk = True
    column_formatters = dict(url=_list_format_links, date=_list_format_date)
    column_list = ('id', 'title', 'date', 'url', 'tags', 'visible')
    column_labels = dict(id='#', title='Project Name', url='URL(s)',
                            tags='Tag(s)', visible='Show?')
    column_sortable_list = ('id', 'title', 'date', 'visible')
    column_searchable_list = ('title', 'date')

    form_args = dict(url=dict(label='Project URL'))


class LinkView(AuthModelView):
    def _list_format_link(view, context, model, name):
        if not getattr(model, name):
            return ''
        return Markup('<a href="{url}" rel="external" target="_blank">{url}</a>'.format(
            url=getattr(model, name)))

    column_formatters = dict(url=_list_format_link)
    column_labels = dict(title='Title', url='URL')


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
admin.add_view(ProjectView(Project, db.session, name='Projects'))
admin.add_view(LinkView(Link, db.session, name='Project: Links'))
admin.add_view(AuthModelView(Tag, db.session, name='Project: Tags'))

path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(CustomFileAdmin(path, '/static/', name='Static Assets', endpoint='static-assets'))
