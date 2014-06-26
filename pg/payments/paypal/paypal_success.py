__author__ = 'krzysztof.maslak'

from flask import Blueprint
from flask import request, session, redirect
paypal_success = Blueprint('paypal_success', __name__, url_prefix='/paypal_success')

@paypal_success.route('/', methods=['GET'])
def process_success():
    paypal_success.logger.info('['+request.remote_addr+'] Paypal success')
    # TODO implement payment-successful.html
    return redirect('/payment-successful.html')