import requests
from pg import resource_bundle, model
from pg.util import security

__author__ = 'krzysztof.maslak'
from flask import Blueprint
from flask import request, session, redirect
paypal_success = Blueprint('paypal_success', __name__, url_prefix='/paypal_success')

@paypal_success.route('/', methods=['GET'])
def process_success():
    paypal_success.logger.info('['+request.remote_addr+'] Paypal success')
    # TODO implement payment-successful.html
    return redirect('/payment-successful.html')

paypal_init = Blueprint('paypal_init', __name__, url_prefix='/paypal/init')


ipn = Blueprint('ipn', __name__, url_prefix='/paypal/ipn')

class IPNNotificationValidation:
    cmd = "_notify-validate"
    verified = "VERIFIED"

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def validate(self, message):
        nvp_string = "cmd=" + self.cmd + "&"
        fullMessage = message.full_message
        nvp_string = nvp_string + fullMessage
        paypal_url = ''
        if self.ioc.get_config()['ENVIRONMENT']=='PRODUCTION':
            paypal_url = self.ioc.get_config()['prod.paypal.url']+"/cgi-bin/webscr"
        else:
            paypal_url = self.ioc.get_config()['paypal.url']+"/cgi-bin/webscr"
        response = requests.post(paypal_url, data=nvp_string)

        if response is not None:
            return response==self.verified and message.payment_status=='Completed'
        return False


class IPNMessageParser:
    def __init__(self, form):
        super().__init__()
        self.form = form

    def parse(self):
        full_message = ''
        for k, v in self.form:
            if len(full_message)>0:
                full_message = full_message+'&'
            full_message = full_message+k+'='+v
        ipn_message = model.ipn.IpnMessage()
        ipn_message.full_message = full_message
        for k, v in self.form:
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

@ipn.route('/', methods=['POST'])
def process_ip():
    ipn_message = IPNMessageParser(request.form).parse()
    ipn.logger.info('IPN received')
    ipn.ioc.new_ipn_message_service().persist(ipn_message)
    notification_validation = IPNNotificationValidation(ipn.ioc)
    if notification_validation.validate(ipn_message):
        ipn_message.validated = True
        ipn.ioc.new_ipn_message_service().merge(ipn_message)
        custom = ipn_message.custom
        payment_reference = security.Security().decrypt(custom)
        data = payment_reference.split("#")
        orderId = int(data[0])
        order = ipn.ioc.new_order_service().find_by_id(orderId);
        if order.order_number==data[1]:
            ipn.ioc.new_payment_processor_service(ipn.logger).process_paid_order(order);

@paypal_init.route('/', methods=['GET'])
def process_init():
    order_id = request.args.get('order_id')
    paypal_init.logger.info('['+request.remote_addr+'] Paypal init [order_id:'+order_id+']')
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
                    for c in range(iv.quantity-1):
                        if iv.shipping_additional is not None:
                            shipping = shipping + iv.shipping_additional
                        else:
                            shipping = shipping + iv.shipping
                if order.offer.currency!=order.currency:
                    basket_items.append({'index':(i+1), 'title':item.title+'('+iv.title+')', 'value':paypal_init.ioc.new_currency_service().convert(order.currency, itotal)})
                else:
                    basket_items.append({'index':(i+1), 'title':item.title+'('+iv.title+')', 'value': itotal})
                i = i+1
        else:
            if order.offer.currency!=order.currency:
                basket_items.append({'index':(i+1), 'title':item.title, 'value':paypal_init.ioc.new_currency_service().convert(order.currency, (item.quantity*(item.net+item.tax)))})
            else:
                basket_items.append({'index':(i+1), 'title':item.title, 'value':(item.quantity*(item.net+item.tax))})
            if item.quantity==1:
                shipping = shipping + item.shipping
            else:
                for c in range(item.quantity-1):
                    if item.shipping_additional is not None:
                        shipping = shipping + item.shipping_additional
                    else:
                        shipping = shipping + item.shipping
            i = i+1
    if order.offer.currency!=order.currency:
        basket_items.append({'index':(i+1), 'title':resource_bundle.ResourceBundle().get_text(order.lang, "shipping"), 'value':paypal_init.ioc.new_currency_service().convert(order.currency, shipping)})
    else:
        basket_items.append({'index':(i+1), 'title':resource_bundle.ResourceBundle().get_text(order.lang, "shipping"), 'value':shipping})

    seller = paypal_init.ioc.get_config()['paypal.seller']
    paypal_url = paypal_init.ioc.get_config()['paypal.url']
    ipn_host = paypal_init.ioc.get_config()['address.www']
    paypal_init.logger.info('['+request.remote_addr+'] Paypal generating html [order_id:'+order_id+']')
    return paypal_init.ioc.new_paypal_service().generate_init_html(order, payment_reference, basket_items, ipn_host, seller, paypal_url)

