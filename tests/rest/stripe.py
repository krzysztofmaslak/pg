from flask import json

__author__ = 'xxx'

from flask.ext.testing import TestCase as Base
from tests import base
from pg import model, app as application
import mock

class StripeTest(Base):
    environ_base={'REMOTE_ADDR': '127.0.0.1'}

    def create_app(self):
        self.ioc = base.TestServiceFactory()
        self.application = application.App(self.ioc)
        app = self.application.create_app()
        app.testing = True
        self.client = app.test_client()
        return app

    def setUp(self):
        self.application.init_db()

    def tearDown(self):
        pass
        # db.session.remove()
        # db.drop_all()

    def test_process(self):
        mock_charge = mock.MagicMock(return_value=base.An(id=123))
        mock_save = mock.MagicMock()
        mock_process_paid_order = mock.MagicMock()
        self.ioc.new_stripe_service = mock.MagicMock(return_value=base.An(charge= mock_charge, save= mock_save))
        self.ioc.new_payment_processor_service = mock.MagicMock(return_value=base.An(process_paid_order= mock_process_paid_order))
        u = model.User('admin', 'password')
        o = model.Offer(u)
        o.currency = 'eur'
        o.status = 1
        o1 = model.OfferItem(o, "My offer item", 2)
        o2 = model.OfferItem(o, "My offer item2")
        blue = model.OfferItemVariation(o2, "Blue", 3)
        red = model.OfferItemVariation(o2, "Red", 1)
        o2.variations = [blue, red]
        o.items.append(o1)
        o.items.append(o2)
        model.base.db.session.add(u)
        model.base.db.session.add(o)
        model.base.db.session.commit()

        order = model.Order()
        order.offer_id = o.id
        or1 = model.OrderItem(order, 'Strings', 1, 10.32, 0, 1.65)
        or1.shipping_additional = 1
        or1.offer_item_id = o1.id
        order.items.append(or1)
        oi = model.OrderItem(order, 'Toy', 0, 0, 0, 0)
        oi.offer_item_id = o2.id
        orv1 = model.OrderItemVariation(oi, "Big", 1, 11.21, 0, 1.65)
        orv1.shipping_additional = 1
        orv1.offer_item_variation_id = blue.id
        oi.variations.append(orv1)
        order.items.append(oi)
        model.base.db.session.add(order)
        model.base.db.session.commit()

        items = [base.An(id=o1.id, quantity=1, variations=[])]
        payment = base.An(offer_id=o.id, subscribe=True, payment_method='cc', currency='eur', country='fr', lang='eng', session_id='kdkdkdkd', items=items)
        payment.billing = base.An(first_name='Mickey', last_name='Mouse', address1='Withworth', address2='Drumcondra', country='ie', city='Dublin', postal_code='10', county='Dublin', email='dublin.krzysztof.maslak@gmail.com', same_address=False)
        payment.shipping = base.An(first_name='Chuck', last_name='Norris', address1='South Central', address2='Rockbrook', country='ie', city='Dublin', postal_code='18', county='Dublin', email='krzysztof.maslak@123.ie', company='Spreadline', phone_number='0842342342')

        r = self.client.post('/rest/payment/', data=json.dumps(payment.as_json()), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(r.json['id'])
        r = self.client.post('/rest/stripe/process', data=json.dumps({'order_id': r.json['id'], 'stripe_token': 'cardToken'}), content_type='application/json', headers=[('Content-Type', 'application/json')],
                             environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        mock_process_paid_order.assert_called_once_with(order)