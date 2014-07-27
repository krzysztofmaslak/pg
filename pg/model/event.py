__author__ = 'root'

import datetime
from pg.model import base

class Event(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    ip = base.db.Column(base.db.String(10))
    creation_date = base.db.Column(base.db.DateTime)
    hash = base.db.Column(base.db.String(15))
    account_id = base.db.Column(base.db.Integer, base.db.ForeignKey('account.id'))
    account = base.db.relationship('Account',
        backref=base.db.backref('events', lazy='dynamic'))

    def __init__(self, ip, account, hash=None):
        self.creation_date=datetime.datetime.now()
        self.ip = ip
        self.account = account
        self.hash = hash

    def _as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['account'])
