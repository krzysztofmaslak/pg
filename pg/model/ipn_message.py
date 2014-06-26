from pg.app import db

__author__ = 'root'


class IpnMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    validated = db.Column(db.Boolean)
    full_message = db.Column(db.Text)
    transaction_type = db.Column(db.String(30))
    payment_status = db.Column(db.String(30))
    mc_gross = db.Column(db.Float)
    mc_currency = db.Column(db.String(3))
    custom = db.Column(db.String(30))
    item_number = db.Column(db.String(10))
    subscr_id = db.Column(db.String(10))
    payer_email = db.Column(db.String(50))





