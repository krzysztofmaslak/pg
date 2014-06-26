import datetime
from pg.model import base

__author__ = 'xxx'


class Account(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    creation_date = base.db.Column(base.db.DateTime)
    properties = base.db.relationship('Property', backref='account', lazy='dynamic')

    def __init__(self, creation_date=datetime.datetime.now()):
        self.creation_date = creation_date

    def __repr__(self):
        return '<Account %r>' % self.id

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude="properties")