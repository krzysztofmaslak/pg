from pg.model import base

__author__ = 'krzysztof.maslak'

class InvoiceIssuer(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    name = base.db.Column(base.db.String(50))
    address = base.db.Column(base.db.String(50))
    city = base.db.Column(base.db.String(50))
    vat_number = base.db.Column(base.db.String(50))
    country = base.db.Column(base.db.String(50))
    invoice_id = base.db.Column(base.db.Integer, base.db.ForeignKey('invoice.id'))

    def __init__(self, name, address, city, vat_number, country):
        self.name = name
        self.address = address
        self.city = city
        self.vat_number = vat_number
        self.country = country