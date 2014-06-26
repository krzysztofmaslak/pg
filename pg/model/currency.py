from pg.model.base import JsonSerializable

__author__ = 'krzysztof.maslak'

from ..app import db

class Currency(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3))
    active = db.Column(db.Integer)

    def __init__(self, code, active):
        self.code = code
        self.active = active

    def __repr__(self):
        return '<Currency %r>' % self.code

