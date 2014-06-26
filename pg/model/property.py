import datetime
from pg.model import base

__author__ = 'xxx'

class Property(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    section = base.db.Column(base.db.String(30))
    code = base.db.Column(base.db.String(30))
    value = base.db.Column(base.db.String(50))
    account_id = base.db.Column(base.db.Integer, base.db.ForeignKey('account.id'))

    def __init__(self, account, section, code, value):
        self.account = account
        self.section = section
        self.code = code
        self.value = value