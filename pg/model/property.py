import datetime
from pg.model.base import JsonSerializable

__author__ = 'xxx'

from ..app import db

class Property(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(30))
    code = db.Column(db.String(30))
    value = db.Column(db.String(50))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __init__(self, account, section, code, value):
        self.account = account
        self.section = section
        self.code = code
        self.value = value