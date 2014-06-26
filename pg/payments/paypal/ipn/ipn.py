from pg.util.security import Security

__author__ = 'krzysztof.maslak'

from pg.payments.paypal.ipn import IPNMessageParser, IPNNotificationValidation
from pg.payments import PaymentProcessor
from flask import Blueprint
from flask import request, session, redirect
ipn = Blueprint('ipn', __name__, url_prefix='/paypal/ipn')

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
        payment_reference = Security().decrypt(custom)
        data = payment_reference.split("#")
        orderId = int(data[0])
        order = ipn.ioc.new_order_service().find_by_id(orderId);
        if order.order_number==data[1]:
            PaymentProcessor(ipn.logger, ipn.ioc).process_paid_order(order);
