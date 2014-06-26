__author__ = 'krzysztof.maslak'

import traceback
import sys
from werkzeug.exceptions import BadRequest
from flask import Blueprint, jsonify
from flask import request, session
stripe_rest = Blueprint('stripe_rest', __name__, url_prefix='/rest/stripe')

def find_order_total(order):
    total = stripe_rest.ioc.new_order_service().find_order_total(order)
    if order.offer.currency!=order.currency:
        # TODO do currency conversion
        # return stripe_rest.ioc.new_currency_service().convert(order.currency, total);
        pass
    else:
        return total

@stripe_rest.route('/process', methods=['POST'])
def process():
    stripe_rest.logger.info('['+request.remote_addr+'] Process payment with stripe for order:'+str(request.json['order_id']))
    order = stripe_rest.ioc.new_order_service().find_by_id(int(request.json['order_id']))
    if order is not None:
        stripe_rest.logger.info('['+request.remote_addr+'] Order='+str(order.id))
        amount = find_order_total(order)
        currency = order.currency.lower()
        try:
            stripe_rest.logger.info('['+request.remote_addr+'] stripe charge order=%s, amount=%s'%(request.json['order_id'], amount))
            resp = stripe.ioc.new_stripe_service().charge(
                amount=int(amount*100),
                currency=currency,
                card=request.json['stripe_token'],
                description=order.order_number
            )
            stripe_rest.logger.info('['+request.remote_addr+'] Success - stripe response '+str(resp)+' order number: '+order.order_number)
            stripe_message = StripeMessage(resp.id, str(resp), resp.order_id)
            stripe.ioc.new_stripe_service().save(stripe_message)
            stripe.ioc.new_payment_processor_service(stripe_rest.logger).process_paid_order(order)
        except:
            traceback.print_exc(file=sys.stdout)
            raise BadRequest('['+request.remote_addr+'] Failed to collect payment')
