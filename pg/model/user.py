import datetime
from pg.model import base

__author__ = 'xxx'

class User(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    username = base.db.Column(base.db.String(50), unique=True)
    password = base.db.Column(base.db.String(50))
    creation_date = base.db.Column(base.db.DateTime)
    active = base.db.Column(base.db.Boolean)
    reset_hash = base.db.Column(base.db.String(50))
    account_id = base.db.Column(base.db.Integer, base.db.ForeignKey('account.id'))
    account = base.db.relationship('Account',
        backref=base.db.backref('users', lazy='dynamic'))

    def __init__(self, username, password, creation_date=datetime.datetime.now()):
        self.username = username
        self.password = password
        self.creation_date = creation_date
        self.active = False

    def __repr__(self):
        return '<User %r>' % self.username

    def _as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['account', 'password'])


