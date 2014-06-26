from pg.model import base

__author__ = 'root'


class IpnMessage(base.db.Model):
    id = base.db.Column(base.db.Integer, primary_key=True)
    date = base.db.Column(base.db.DateTime)
    validated = base.db.Column(base.db.Boolean)
    full_message = base.db.Column(base.db.Text)
    transaction_type = base.db.Column(base.db.String(30))
    payment_status = base.db.Column(base.db.String(30))
    mc_gross = base.db.Column(base.db.Float)
    mc_currency = base.db.Column(base.db.String(3))
    custom = base.db.Column(base.db.String(30))
    item_number = base.db.Column(base.db.String(10))
    subscr_id = base.db.Column(base.db.String(10))
    payer_email = base.db.Column(base.db.String(50))





