import datetime
from pg.model import base

__author__ = 'krzysztof.maslak'


class Contact(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    creation_date = base.db.Column(base.db.DateTime)
    email = base.db.Column(base.db.String(50))
    message = base.db.Column(base.db.Text)
    ip = base.db.Column(base.db.String(50))
    account_id = base.db.Column(base.db.Integer, base.db.ForeignKey('account.id'))
    account = base.db.relationship('Account',
        backref=base.db.backref('contacts', lazy='dynamic'))

    def __init__(self, ip, email, message, creation_date=datetime.datetime.now()):
        self.creation_date = creation_date
        self.ip = ip
        self.email = email
        self.message = message

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['account'])





    