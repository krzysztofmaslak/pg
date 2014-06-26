from pg.model import base

__author__ = 'krzysztof.maslak'

import datetime

class Invoice(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    creation_date = base.db.Column(base.db.DateTime)
    reference_number = base.db.Column(base.db.String(50))
    invoice_number = base.db.Column(base.db.String(50))
    issue_city = base.db.Column(base.db.String(50))
    total_gross = base.db.Column(base.db.String(50))
    issuers = base.db.relationship('InvoiceIssuer', backref='invoice', lazy='dynamic')

    def __init__(self):
        self.creation_date=datetime.datetime.now()

