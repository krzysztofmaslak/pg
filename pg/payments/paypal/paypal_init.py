from pg.resource_bundle import ResourceBundle
from pg.util.security import Security

__author__ = 'krzysztof.maslak'
from flask import Blueprint
from flask import request, session, redirect
paypal_init = Blueprint('paypal_init', __name__, url_prefix='/paypal/init')

@paypal_init.route('/', methods=['GET'])
def process_init():
    order_id = request.args.get('offer_id')
    paypal_init.logger.info('['+request.remote_addr+'] Paypal init [order_id:'+order_id+']')
    order = paypal_init.ioc.new_order_service().find_by_id(int(order_id))
    payment_reference = Security().encrypt(order.id+"#"+order.order_number)

    html = """<html>
                <head></head>
                <body>"""
    i = 0
    shipping = 0.0
    basket_items = ''
    for i in order.items:
        if i.variations is not None and len(i.variations)>0:
            basket_items = basket_items+"""<input type="hidden" name="item_name_"""+(i+1)+'" value="'+i.title+'"/>'
            itotal = 0.0
            for iv in i.variations:
                itotal = itotal+(iv.quantity*iv.total)
                if iv.quantity==1:
                    shipping = shipping + iv.shipping
                else:
                    for c in range(iv.quantity-1):
                        shipping = shipping + iv.shipping_additional
            basket_items = basket_items+'<input type="hidden" name="amount_"'+(i+1)+'" value="'+ paypal_init.ioc.new_currency_service().convert(order.currency, itotal)+'"/>'
        else:
            basket_items = basket_items+"""<input type="hidden" name="item_name_"""+(i+1)+'" value="'+i.title+'"/>'
            basket_items = basket_items+'<input type="hidden" name="amount_"'+(i+1)+'" value="'+ paypal_init.ioc.new_currency_service().convert(order.currency, (i.quantity*i.total))+'"/>'
            if i.quantity==1:
                shipping = shipping + i.shipping
            else:
                for c in range(i.quantity-1):
                    shipping = shipping + i.shipping_additional
        i = i+1
    resource_bundle = ResourceBundle()
    basket_items = basket_items+'<input type="hidden" name="item_name_"'+(i+1)+'" value="'+resource_bundle.get_text(order.lang, "shipping")+'"/>'
    basket_items = basket_items+'<input type="hidden" name="amount_"'+(i+1)+'" value="'+paypal_init.ioc.new_currency_service().convert(order.currency, shipping)+'"/>'
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

    html = html+"""<div>
            <form id="paypalForm" action='"""+paypal_url+'/cgi-bin/webscr" method="post">'+"""
            <input type="hidden" name="cmd" value="_cart"/>
            <input type="hidden" name="custom" value='"""+payment_reference+"""'/>
            <input type="hidden" name="upload" value="1"/>
            <input type="hidden" name="business" value='"""+seller+"""'/>
            <input type="hidden" name="currency_code" id="currency_code" value='"""+order.currency+"""'/>
            """+basket_items+"""
            <input type="hidden" name="item_number" value="BB-PROD1"/>
            <input type="hidden" name="notify_url" value='"""+ipn_host+"""/pg/paypal/ipn'/>"""
    b = order.billing.first()
    html = html + """<input type="hidden" name="country_code" value='"""+b.country+"""'/>
        <input type="hidden" name="address1" value='"""+b.address1+"""'/>
        <input type="hidden" name="address2" value='"""+b.address2+"""'/>
        <input type="hidden" name="city" value='"""+b.city+"""'/>"""
    if b.county is not None and len(b.county)!=0:
        html = html + "<input type=\"hidden\" name=\"county\" value=\""+b.county+"\"/>"
    if b.postal_code is not None and len(b.postal_code)!=0:
        html = html + "<input type=\"hidden\" name=\"zip\" value=\""+b.postal_code+"\"/>"
    html = html+"""<input type="hidden" name="email" value='"""+b.email+"""'/>
    <input type="hidden" name="first_name" value='"""+b.first_name+"""'/>
    <input type="hidden" name="last_name" value='"""+b.last_name+"""'/>
    <input type="hidden" name="payer_email" value='"""+b.email+"""'/>
    <input type="hidden" name="payer_id" value='"""+b.id+"""'/>
    <script type="text/javascript">document.getElementById('paypalForm').submit()</script>
    </form>
    </div>
    </body>
    </html>"""
