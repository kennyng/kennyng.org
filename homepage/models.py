from datetime import datetime
from homepage import db


tags = db.Table('tags',
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
        db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    url = db.Column(db.String(255))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    visible = db.Column(db.Boolean, default=True)

    links = db.relationship('Link', backref='project', lazy='select')
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('projects', lazy='dynamic'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    def __repr__(self):
        return '<Project: {}>'.format(self.title)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    url = db.Column(db.String(255))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return '<Link: {} [{}]>'.format(self.title, self.url)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)


