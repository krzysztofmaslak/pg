import datetime
from pg.model import base

__author__ = 'xxx'

class Withdrawal(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    amount = base.db.Column(base.db.Float)
    iban = base.db.Column(base.db.String(50))
    bic = base.db.Column(base.db.String(15))
    creation_date = base.db.Column(base.db.DateTime)
    status = base.db.Column(base.db.Boolean)
    account_id = base.db.Column(base.db.Integer, base.db.ForeignKey('account.id'))
    account = base.db.relationship('Account',
        backref=base.db.backref('withdrawals', lazy='dynamic'))

    def __init__(self, amount, iban, bic, creation_date=datetime.datetime.now()):
        self.amount = amount
        self.iban = iban
        self.bic = bic
        self.creation_date = creation_date
        self.status = False

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['account', 'iban', 'bic'])


