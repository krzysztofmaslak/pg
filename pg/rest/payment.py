from collections import namedtuple
import json

__author__ = 'xxx'

from flask import Blueprint, jsonify
from flask import request, session

payment = Blueprint('payment', __name__, url_prefix='/rest/payment')

@payment.route('/', methods=['POST'])
def apply_payment():
    payment.logger.info('['+request.remote_addr+'] Apply payment')
    # TODO handle QuantityNotAvailable
    x = json.loads(json.dumps(request.json), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    order = payment.ioc.new_order_service(payment.logger).save(x)
    return jsonify({'id':order.id})
