import datetime
from pg.model import base

__author__ = 'xxx'

class Property(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    code = base.db.Column(base.db.String(30))
    value = base.db.Column(base.db.String(50))
    account_id = base.db.Column(base.db.Integer, base.db.ForeignKey('account.id'))

    def __init__(self, account, code, value):
        self.account = account
        self.code = code
        self.value = value