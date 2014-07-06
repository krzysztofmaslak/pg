from flask import json

__author__ = 'xxx'

from flask.ext.testing import TestCase as Base
from tests import base
from pg import resource_bundle, model, app as application
from pg.util import security
import mock

class PaypalTest(Base):
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
        mock_paypal_service_generate_init_html=mock.MagicMock(return_value="")
        self.ioc.new_paypal_service = mock.MagicMock(return_value=base.An(generate_init_html=mock_paypal_service_generate_init_html))
        mock_charge = mock.MagicMock(return_value=base.An(id=123))
        mock_save = mock.MagicMock()
        mock_process_paid_order = mock.MagicMock()
        self.ioc.new_stripe_service = mock.MagicMock(return_value=base.An(charge= mock_charge, save= mock_save))
        self.ioc.new_payment_processor_service = mock.MagicMock(return_value=base.An(process_paid_order= mock_process_paid_order))
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        o.currency = 'eur'
        o.status = 1
        o1 = model.OfferItem(o, "My offer item", 2, 3.45, 0, 1.65, 1)
        o2 = model.OfferItem(o, "My offer item2")
        o2.status = 1
        blue = model.OfferItemVariation(o2, "Blue", 3)
        blue.status = 1
        red = model.OfferItemVariation(o2, "Red", 1)
        red.status = 1
        o2.variations = [blue, red]
        o.items.append(o1)
        o.items.append(o2)
        model.base.db.session.add(u)
        model.base.db.session.add(o)
        model.base.db.session.commit()

        items = [base.An(id=o1.id, quantity=1, variations=[])]
        payment = base.An(offer_id=o.id, subscribe=True, payment_method='cc', currency='eur', country='fr', lang='eng', session_id='kdkdkdkd', items=items)
        payment.billing = base.An(first_name='Mickey', last_name='Mouse', address1='Withworth', address2='Drumcondra', country='ie', city='Dublin', postal_code='10', county='Dublin', email='dublin.krzysztof.maslak@gmail.com', same_address=False)
        payment.shipping = base.An(first_name='Chuck', last_name='Norris', address1='South Central', address2='Rockbrook', country='ie', city='Dublin', postal_code='18', county='Dublin', email='krzysztof.maslak@123.ie', company='Spreadline', phone_number='0842342342')

        r = self.client.post('/rest/payment/', data=json.dumps(payment.as_json()), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(r.json['id'])
        order_id = int(r.json['id'])
        r = self.client.get('/paypal/init/?order_id='+str(r.json['id']), environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)

        order = self.ioc.new_order_service().find_by_id(order_id)
        payment_reference = security.Security().encrypt(str(order_id)+"#"+order.order_number)
        seller = self.ioc.get_config()['paypal.seller']
        paypal_url = self.ioc.get_config()['paypal.url']
        ipn_host = self.ioc.get_config()['address.www']
        i = 0
        shipping = 0.0
        basket_items = []
        for item in order.items:
            if item.variations is not None and item.variations.count()>0:
                itotal = 0.0
                for iv in item.variations:
                    itotal = itotal+((iv.quantity*(iv.net+iv.tax)))
                    if iv.quantity==1:
                        shipping = shipping + iv.shipping
                    else:
                        for c in range(iv.quantity-1):
                            shipping = shipping + iv.shipping_additional
                if order.offer.currency!=order.currency:
                    basket_items.append({'index':(i+1), 'title':item.title, 'value':self.ioc.new_currency_service().convert(order.currency, itotal)})
                else:
                    basket_items.append({'index':(i+1), 'title':item.title, 'value': itotal})
            else:
                if order.offer.currency!=order.currency:
                    basket_items.append({'index':(i+1), 'title':item.title, 'value':self.ioc.new_currency_service().convert(order.currency, (item.quantity*(item.net+item.tax)))})
                else:
                    basket_items.append({'index':(i+1), 'title':item.title, 'value':(item.quantity*(item.net+item.tax))})
                if item.quantity==1:
                    shipping = shipping + item.shipping
                else:
                    for c in range(item.quantity-1):
                        shipping = shipping + item.shipping_additional
            i = i+1
        if order.offer.currency!=order.currency:
            basket_items.append({'index':(i+1), 'title':resource_bundle.ResourceBundle().get_text(order.lang, "shipping"), 'value':self.ioc.new_currency_service().convert(order.currency, shipping)})
        else:
            basket_items.append({'index':(i+1), 'title':resource_bundle.ResourceBundle().get_text(order.lang, "shipping"), 'value':shipping})

        mock_paypal_service_generate_init_html.assert_called_once_with(order, payment_reference, basket_items, ipn_host, seller, paypal_url)