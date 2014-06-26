import datetime
from pg.model.base import JsonSerializable


__author__ = 'xxx'

from ..app import db


class Offer(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    title = db.Column(db.String(80))
    hash = db.Column(db.String(80))
    status = db.Column(db.Integer)
    currency = db.Column(db.String(3))

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship('Account', backref=db.backref('offers', lazy='dynamic'))
    items = db.relationship('OfferItem', backref='offer', lazy='dynamic')

    def __init__(self, account, title='', hash='', status=0, currency='', creation_date=datetime.datetime.now()):
        self.title = title
        self.hash = hash
        self.status = status
        self.currency = currency
        self.account_id = account.id
        self.creation_date = creation_date

    def __repr__(self):
        return '<Offer %r>' % self.title

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['account', 'orders'])


