from pg.model.base import JsonSerializable

__author__ = 'krzysztof.maslak'

import datetime
from pg.app import db

class Invoice(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    reference_number = db.Column(db.String(50))
    invoice_number = db.Column(db.String(50))
    issue_city = db.Column(db.String(50))
    total_gross = db.Column(db.String(50))
    issuers = db.relationship('InvoiceIssuer', backref='invoice', lazy='dynamic')

    def __init__(self):
        self.creation_date=datetime.datetime.now()

