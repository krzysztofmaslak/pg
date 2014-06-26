import datetime
from pg.model import base

__author__ = 'krzysztof.maslak'

class CurrencyRate(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    code = base.db.Column(base.db.String(3))
    rate = base.db.Column(base.db.Float)
    last_update = base.db.Column(base.db.DateTime)

    def __init__(self, code, rate, last_update=datetime.datetime.now()):
        self.code = code
        self.rate = rate
        self.last_update = last_update

    def __repr__(self):
        return '<CurrencyRate %r>' % self.code
