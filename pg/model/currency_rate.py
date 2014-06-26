import datetime
from pg.model.base import JsonSerializable

__author__ = 'krzysztof.maslak'

from ..app import db

class CurrencyRate(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3))
    rate = db.Column(db.Float)
    last_update = db.Column(db.DateTime)

    def __init__(self, code, rate, last_update=datetime.datetime.now()):
        self.code = code
        self.rate = rate
        self.last_update = last_update

    def __repr__(self):
        return '<CurrencyRate %r>' % self.code
