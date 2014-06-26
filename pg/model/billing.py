from pg.model import base

__author__ = 'krzysztof.maslak'


class Billing(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    first_name = base.db.Column(base.db.String(50))
    last_name = base.db.Column(base.db.String(50))
    address1 = base.db.Column(base.db.String(50))
    address2 = base.db.Column(base.db.String(50))
    country = base.db.Column(base.db.String(3))
    city = base.db.Column(base.db.String(20))
    postal_code = base.db.Column(base.db.String(10))
    county = base.db.Column(base.db.String(10))
    email = base.db.Column(base.db.String(50))
    same_address = base.db.Column(base.db.Boolean)
    order_id = base.db.Column(base.db.Integer, base.db.ForeignKey('order.id'))





    