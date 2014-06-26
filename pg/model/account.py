import datetime
from ..app import db
from pg.model.base import JsonSerializable

__author__ = 'xxx'


class Account(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    properties = db.relationship('Property', backref='account', lazy='dynamic')

    def __init__(self, creation_date=datetime.datetime.now()):
        self.creation_date = creation_date

    def __repr__(self):
        return '<Account %r>' % self.id

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude="properties")