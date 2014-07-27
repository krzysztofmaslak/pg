from itertools import chain
import urllib
from urllib.request import urlopen
import requests
from pg import resource_bundle, model
from pg.util import security
from pg.util.http_utils import get_customer_ip

__author__ = 'krzysztof.maslak'
from flask import Blueprint, Response
from flask import request, session, redirect
paypal_success = Blueprint('paypal_success', __name__, url_prefix='/paypal_success')

@paypal_success.route('/', methods=['GET'])
def process_success():
    paypal_success.logger.info('['+get_customer_ip()+'] Paypal success')
    # TODO implement payment-successful.html
    return redirect('/payment-successful.html')

paypal_init = Blueprint('paypal_init', __name__, url_prefix='/paypal/init')


ipn = Blueprint('ipn', __name__, url_prefix='/paypal/ipn')

class IPNNotificationValidation:
    cmd = "_notify-validate"
    verified = "VERIFIED"

    def __init__(self, ioc, logger):
        super().__init__()
        self.ioc = ioc
        self.logger = logger

    def validate(self, message, post):
        nvp_string = "cmd=" + self.cmd + "&"
        fullMessage = message.full_message
        nvp_string = nvp_string + fullMessage
        data = urllib.parse.urlencode(post)
        data['cmd']=self.cmd
        data = data.encode('utf-8') # data should be bytes


        paypal_url = self.ioc.get_config()['paypal.url']+"/cgi-bin/webscr"
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(paypal_url, data=data, headers=headers)

        if response is not None:
            self.logger.info("message status: %s"%message.payment_status)
            self.logger.info("message text: %s"%response.text)
            return response.text==self.verified and message.payment_status=='Completed'
        else:
            self.logger.info('NPV message was None')
        return False


class IPNMessageParser:
    def __init__(self, form):
        super().__init__()
        self.form = form

    def parse(self):
        full_message = ''
        for k, v in self.form.items():
            if len(full_message)>0:
                full_message = full_message+'&'
            full_message = full_message+k+'='+v
        ipn_message = model.IpnMessage()
        ipn_message.full_message = full_message
        for k, v in self.form.items():
            self.add_variable(ipn_message, k, v)
        return ipn_message

    def add_variable(self, ipn_message, name, value):
        if name=="txn_type":
            ipn_message.transaction_type = value
        elif name=='payment_status':
            ipn_message.payment_status = value
        elif name=='mc_gross':
            ipn_message.mc_gross = value
        elif name=='mc_currency':
            ipn_message.mc_currency = value
        elif name=='item_number':
            ipn_message.item_number = value
        elif name=='custom':
            ipn_message.custom = value
        elif name=='txn_id':
            ipn_message.txn_id=value
        elif name=='subscr_id':
            ipn_message.subscr_id=value
        elif name=='payer_email':
            ipn_message.payer_email = value

def ordered_storage(f):
    import werkzeug.datastructures
    import flask
    def decorator(*args, **kwargs):
        flask.request.parameter_storage_class = werkzeug.datastructures.ImmutableOrderedMultiDict
        return f(*args, **kwargs)
    return decorator

@ipn.route('/', methods=['POST'])
@ordered_storage
def process_ip():
    ipn.logger.info('IPN received')
    ipn_message = IPNMessageParser(request.form).parse()
    ipn.ioc.new_ipn_message_service().persist(ipn_message)
    IPN_VERIFY_EXTRA_PARAMS = (('cmd', '_notify-validate'),)
     #probably should have a sanity check here on the size of the form data to guard against DoS attacks
    verify_args = chain(request.form.items(), IPN_VERIFY_EXTRA_PARAMS)
    verify_string = '&'.join(('%s=%s' % (param, value) for param, value in verify_args))
    #req = Request(verify_string)
    ipn.logger.info("verify string type: %s"%type(verify_string.encode('utf-8')))
    paypal_url = ipn.ioc.get_config()['paypal.url']+'/cgi-bin/webscr'
    ipn.logger.info('paypal url:%s'%paypal_url)
    response = urlopen(paypal_url, data=verify_string.encode('utf-8'))
    status = response.read().decode(encoding='UTF-8')
    ipn.logger.info("IPN verification status: %s"%status)

    if status == 'VERIFIED' and ipn_message.payment_status=='Completed':
        ipn.logger.info("PayPal transaction was verified successfully.")
        ipn_message.validated = True
        ipn.ioc.new_ipn_message_service().merge(ipn_message)
        custom = ipn_message.custom
        payment_reference = security.Security().decrypt(custom)
        data = payment_reference.split("#")
        orderId = int(data[0])
        order = ipn.ioc.new_order_service().find_by_id(orderId);
        if order.order_number==data[1]:
            ipn.ioc.new_payment_processor_service().process_paid_order(order)
            ipn.logger.info('IPN processed')
            return Response(status=200)
    else:
        ipn.logger.info('IPN validation failed')
    return Response(status=500)

@paypal_init.route('/', methods=['GET'])
def process_init():
    order_id = request.args.get('order_id')
    paypal_init.logger.info('['+get_customer_ip()+'] Paypal init [order_id:'+order_id+']')
    order = paypal_init.ioc.new_order_service().find_by_id(int(order_id))
    payment_reference = security.Security().encrypt(str(order.id)+"#"+order.order_number)
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
                    shipping = shipping + iv.shipping
                    for c in range(iv.quantity-1):
                        if iv.shipping_additional is not None:
                            shipping = shipping + iv.shipping_additional
                        else:
                            shipping = shipping + iv.shipping
                if order.offer.currency!=order.currency:
                    basket_items.append({'index':(i+1), 'title':item.title+'('+iv.title+')', 'value':round(paypal_init.ioc.new_currency_service().convert(order.currency, itotal), 2)})
                else:
                    basket_items.append({'index':(i+1), 'title':item.title+'('+iv.title+')', 'value': round(itotal, 2)})
                i = i+1
        else:
            if order.offer.currency!=order.currency:
                basket_items.append({'index':(i+1), 'title':item.title, 'value':round(paypal_init.ioc.new_currency_service().convert(order.currency, (item.quantity*(item.net+item.tax))), 2)})
            else:
                basket_items.append({'index':(i+1), 'title':item.title, 'value':round((item.quantity*(item.net+item.tax)), 2)})
            if item.quantity==1:
                shipping = shipping + item.shipping
            else:
                shipping = shipping + item.shipping
                for c in range(item.quantity-1):
                    if item.shipping_additional is not None:
                        shipping = shipping + item.shipping_additional
                    else:
                        shipping = shipping + item.shipping
            i = i+1
    if order.offer.currency!=order.currency:
        basket_items.append({'index':(i+1), 'title':resource_bundle.ResourceBundle().get_text(order.lang, "shipping"), 'value':round(paypal_init.ioc.new_currency_service().convert(order.currency, shipping), 2)})
    else:
        basket_items.append({'index':(i+1), 'title':resource_bundle.ResourceBundle().get_text(order.lang, "shipping"), 'value':round(shipping, 2)})

    seller = paypal_init.ioc.get_config()['paypal.seller']
    paypal_url = paypal_init.ioc.get_config()['paypal.url']
    ipn_host = paypal_init.ioc.get_config()['address.www']
    paypal_init.logger.info('['+get_customer_ip()+'] Paypal generating html [order_id:'+order_id+']')
    return paypal_init.ioc.new_paypal_service().generate_init_html(order, payment_reference, basket_items, ipn_host, seller, paypal_url)

