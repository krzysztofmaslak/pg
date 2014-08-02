import datetime
from pg.model import base

__author__ = 'xxx'


class Account(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    creation_date = base.db.Column(base.db.DateTime)
    properties = base.db.relationship('Property', backref='account', lazy='dynamic')
    name = base.db.Column(base.db.String(30))
    lang = base.db.Column(base.db.String(3))
    hash = base.db.Column(base.db.String(15))
    balance = base.db.Column(base.db.Float)

    def __init__(self, creation_date=datetime.datetime.now()):
        self.creation_date = creation_date
        self.balance = 0

    def __repr__(self):
        return '<Account %r>' % self.id

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude="properties")