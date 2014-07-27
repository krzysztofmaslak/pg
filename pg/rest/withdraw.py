import json
from pg import model
from pg.rest import base
from pg.util.http_utils import get_customer_ip

__author__ = 'xxx'

from flask import Blueprint, jsonify, Response
from flask import request, session
from pg import resource_bundle
withdraw = Blueprint('withdraw', __name__, url_prefix='/rest/withdraw')

@withdraw.route('/balance')
@base.authenticated
def balance():
    user = withdraw.ioc.new_user_service().find_by_username(session['username'])
    js = { "balance" : user.account.balance, "withdrawals" : [o.as_json() for o in user.account.withdrawals]}
    return Response(json.dumps(js),  mimetype='application/json')

@withdraw.route('/request', methods=['POST'])
@base.authenticated
def request_withdrawal():
    withdraw.logger.debug('['+get_customer_ip()+'] processing withdrawal request for user %s'%(session['username']))
    user = withdraw.ioc.new_user_service().find_by_username(session['username'])
    amount = request.json['amount']
    iban = request.json['iban']
    bic = request.json['bic']

    if user.account.balance>=amount:
        user.account.balance = user.account.balance - amount
        model.base.db.session.commit()
        withdraw.ioc.new_withdrawal_service().save(model.Withdrawal(amount, iban, bic))
        js = { "balance" : user.account.balance, "withdrawals" : [o.as_json() for o in user.account.withdrawals] }
        return Response(json.dumps(js),  mimetype='application/json', status=200)
    else:
        withdraw.logger.debug('['+get_customer_ip()+'] not enough funds to make withdrawal for user %s'%(session['username']))
        messages = resource_bundle.ResourceBundle()
        js = { "msg" : messages.get_text(user.account.lang, 'not_enough_funds')}
        return Response(json.dumps(js),  mimetype='application/json', status=400)