from pg import resource_bundle
from pg.util import security

__author__ = 'krzysztof.maslak'
from flask import Blueprint
from flask import request, session, redirect
paypal_init = Blueprint('paypal_init', __name__, url_prefix='/paypal/init')

@paypal_init.route('/', methods=['GET'])
def process_init():
    order_id = request.args.get('order_id')
    paypal_init.logger.info('['+request.remote_addr+'] Paypal init [order_id:'+order_id+']')
    order = paypal_init.ioc.new_order_service().find_by_id(int(order_id))
    payment_reference = security.Security().encrypt(order.id+"#"+order.order_number)
    i = 0
    shipping = 0.0
    basket_items = []
    for i in order.items:
        if i.variations is not None and len(i.variations)>0:
            itotal = 0.0
            for iv in i.variations:
                itotal = itotal+(iv.quantity*iv.total)
                if iv.quantity==1:
                    shipping = shipping + iv.shipping
                else:
                    for c in range(iv.quantity-1):
                        shipping = shipping + iv.shipping_additional
            basket_items.append({'index':(i+1), 'title':i.title, 'value':paypal_init.ioc.new_currency_service().convert(order.currency, itotal)})
        else:
            basket_items.append({'index':(i+1), 'title':i.title, 'value':paypal_init.ioc.new_currency_service().convert(order.currency, (i.quantity*i.total))})
            if i.quantity==1:
                shipping = shipping + i.shipping
            else:
                for c in range(i.quantity-1):
                    shipping = shipping + i.shipping_additional
        i = i+1
    basket_items.append({'index':(i+1), 'title':resource_bundle.ResourceBundle().get_text(order.lang, "shipping"), 'value':paypal_init.ioc.new_currency_service().convert(order.currency, shipping)})

    ipn_host = ''
    seller = ''
    paypal_url = ''
    if paypal_init.ioc.get_config()['ENVIRONMENT']=='PRODUCTION':
        seller = paypal_init.ioc.get_config()['prod.paypal.seller']
        paypal_url = paypal_init.ioc.get_config()['prod.paypal.url']
        ipn_host = paypal_init.ioc.get_config()['address.www']
    else:
        seller = paypal_init.ioc.get_config()['paypal.seller']
        paypal_url = paypal_init.ioc.get_config()['paypal.url']
        ipn_host = paypal_init.ioc.get_config()['address.www']
    return paypal_init.ioc.new_paypal_service().generate_init_html(order, payment_reference, basket_items, ipn_host, seller, paypal_url)

