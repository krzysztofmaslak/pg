from ..app import db
from pg.model.base import JsonSerializable

__author__ = 'krzysztof.maslak'


class Country(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3))

    def __init__(self, code):
        self.code = code