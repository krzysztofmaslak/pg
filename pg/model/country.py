from pg.model import base

__author__ = 'krzysztof.maslak'


class Country(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    code = base.db.Column(base.db.String(3))

    def __init__(self, code):
        self.code = code