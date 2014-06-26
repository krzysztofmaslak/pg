from ..app import db
from pg.model.base import JsonSerializable

__author__ = 'krzysztof.maslak'


class Billing(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address1 = db.Column(db.String(50))
    address2 = db.Column(db.String(50))
    country = db.Column(db.String(3))
    city = db.Column(db.String(20))
    postal_code = db.Column(db.String(10))
    county = db.Column(db.String(10))
    email = db.Column(db.String(50))
    same_address = db.Column(db.Boolean)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))





    