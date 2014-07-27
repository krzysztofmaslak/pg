import math

__author__ = 'krzysztof.maslak'

from pg import model
import traceback
import sys
from werkzeug.exceptions import BadRequest
from flask import Blueprint, jsonify, Response
from flask import request, session
stripe_rest = Blueprint('stripe_rest', __name__, url_prefix='/rest/stripe')

def find_order_total(order):
    total = stripe_rest.ioc.new_order_service().find_order_total(order)
    if order.offer.currency!=order.currency:
        stripe_rest.logger.info('['+get_customer_ip()+'] doing currency exchange=[%s>%s]'+(order.offer.currency, order.currency))
        # TODO do currency conversion
        # return stripe_rest.ioc.new_currency_service().convert(order.currency, total);
        pass
    else:
        return total

@stripe_rest.route('/process', methods=['POST'])
def process():
    stripe_rest.logger.info('['+get_customer_ip()+'] Process payment with stripe for order:'+str(request.json['order_id']))
    order = stripe_rest.ioc.new_order_service().find_by_id(int(request.json['order_id']))
    if order is not None:
        stripe_rest.logger.info('['+get_customer_ip()+'] Order='+str(order.id))
        amount = find_order_total(order)
        currency = order.currency.lower()
        try:
            stripe_rest.logger.info('['+get_customer_ip()+'] stripe charge order=%s, amount=%s'%(request.json['order_id'], amount))

            resp = stripe_rest.ioc.new_stripe_service().charge(
                amount=int(math.ceil(amount*100)),
                currency=currency,
                card=request.json['stripe_token'],
                description=order.order_number
            )
            stripe_rest.logger.info('['+get_customer_ip()+'] Success - stripe response '+str(resp)+' order number: '+order.order_number)
            stripe_message = model.StripeMessage(resp.id, str(resp), int(request.json['order_id']))
            stripe_rest.ioc.new_stripe_service().save(stripe_message)
            stripe_rest.ioc.new_payment_processor_service().process_paid_order(order)
            return Response(status=200)
        except:
            traceback.print_exc(file=sys.stdout)
            raise BadRequest('['+get_customer_ip()+'] Failed to collect payment')
