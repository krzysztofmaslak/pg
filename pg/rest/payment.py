from collections import namedtuple
import json
from pg.util.http_utils import get_customer_ip
from pg import wsgi
__author__ = 'xxx'

from flask import Blueprint, jsonify
from flask import request, session

payment = Blueprint('payment', __name__, url_prefix='/rest/payment')

@payment.route('/', methods=['POST'])
@wsgi.catch_exceptions
def apply_payment():
    payment.logger.info('['+get_customer_ip()+'] Apply payment for order: %s'%json.dumps(request.json))
    # TODO handle QuantityNotAvailable
    x = json.loads(json.dumps(request.json), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    order = payment.ioc.new_order_service().save(x)
    return jsonify({'id':order.id, 'order_number': order.order_number})
