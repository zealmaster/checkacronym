from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64),  nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(64), index=True)
    adds = db.relationship('Create', backref='author', lazy='dynamic')


class Create(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(500),  index=True)
    meaning = db.Column(db.String(10000), nullable=True)
    definition = db.Column(db.String(10000), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

