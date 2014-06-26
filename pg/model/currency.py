from pg.model import base

__author__ = 'krzysztof.maslak'


class Currency(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    code = base.db.Column(base.db.String(3))
    active = base.db.Column(base.db.Integer)

    def __init__(self, code, active):
        self.code = code
        self.active = active

    def __repr__(self):
        return '<Currency %r>' % self.code

