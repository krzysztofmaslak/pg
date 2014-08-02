import datetime
from pg.model import base


__author__ = 'xxx'


class Offer(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    creation_date = base.db.Column(base.db.DateTime)
    title_en = base.db.Column(base.db.String(80))
    title_fr = base.db.Column(base.db.String(80))
    hash = base.db.Column(base.db.String(15))
    status = base.db.Column(base.db.Integer)
    currency = base.db.Column(base.db.String(3))
    
    account_id = base.db.Column(base.db.Integer, base.db.ForeignKey('account.id'))
    account = base.db.relationship('Account', backref=base.db.backref('offers', lazy='dynamic'))
    items = base.db.relationship('OfferItem', backref='offer', lazy='dynamic')

    def __init__(self, account, title_en='', title_fr='', hash='', status=0, currency='', creation_date=datetime.datetime.now()):
        self.title_en = title_en
        self.title_fr = title_fr
        self.hash = hash
        self.status = status
        self.currency = currency
        self.account = account
        self.creation_date = creation_date

    def __repr__(self):
        return '<Offer %r>' % self.title

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['account', 'orders'])


