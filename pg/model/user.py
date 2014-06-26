import datetime
from pg.model.base import JsonSerializable

__author__ = 'xxx'

from ..app import db

class User(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship('Account',
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, password, creation_date=datetime.datetime.now()):
        self.username = username
        self.password = password
        self.creation_date = creation_date

    def __repr__(self):
        return '<User %r>' % self.username

    def _as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['account', 'password'])


