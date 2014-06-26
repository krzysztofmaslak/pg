from pg.model.base import JsonSerializable

__author__ = 'krzysztof.maslak'

import datetime
from pg.app import db

class InvoiceIssuer(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    vat_number = db.Column(db.String(50))
    country = db.Column(db.String(50))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))

    def __init__(self, name, address, city, vat_number, country):
        self.name = name
        self.address = address
        self.city = city
        self.vat_number = vat_number
        self.country = country