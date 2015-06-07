from datetime import datetime
import re
from unicodedata import normalize
from web import db


_slug_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    title = db.Column(db.String(120))
    url = db.Column(db.String(255))
    image = db.Column(db.String(255))

    def __repr__(self):
        return '<Book: ({}) {}>'.format(self.id, self.title)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(10))
    title = db.Column(db.String(80))
    tagline = db.Column(db.String(255))
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    info = db.Column(db.String(255))
    code = db.Column(db.String(255))
    image = db.Column(db.String(255))

    def __repr(self):
        return '<Project: {}>'.format(self.title)


tags = db.Table('tags',
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
        db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())
    is_published = db.Column(db.Boolean)

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title="", description="", content="", pub_date=None, is_published=False, tags=[]):
        self.title = title
        self.description = description
        self.content = content
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.is_published = is_published
        self.tags = tags

    def __repr__(self):
        return '<Post: {}>'.format(self.title)

    @property
    def slugify(self, delim=b'-'):
        result = []
        for word in _slug_re.split(self.title.lower()):
            word = normalize('NFKD', word).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return str(delim.join(result), 'utf_8')

    @property
    def humanized_date(self):
        return self.pub_date.strftime('%B %d, %Y')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)
