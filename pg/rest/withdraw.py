import json
from pg import model
from pg.rest import base

__author__ = 'xxx'

from flask import Blueprint, jsonify, Response
from flask import request, session
from pg import resource_bundle
withdraw = Blueprint('withdraw', __name__, url_prefix='/rest/withdraw')

@withdraw.route('/balance')
@base.authenticated
def balance():
    user = withdraw.ioc.new_user_service().find_by_username(session['username'])
    js = { "balance" : user.account.balance}
    return Response(json.dumps(js),  mimetype='application/json')

@withdraw.route('/request', methods=['POST'])
@base.authenticated
def request_withdrawal():
    withdraw.logger.debug('['+request.remote_addr+'] processing withdrawal request for user %s'%(session['username']))
    user = withdraw.ioc.new_user_service().find_by_username(session['username'])
    print('amount %s'%request.json)
    amount = request.json['amount']
    iban = request.json['iban']
    bic = request.json['bic']

    if user.account.balance>=amount:
        withdraw.ioc.new_withdrawal_service().save(model.Withdrawal(amount, iban, bic))
        return Response(status=200)
    else:
        withdraw.logger.debug('['+request.remote_addr+'] not enough funds to make withdrawal for user %s'%(session['username']))
        messages = resource_bundle.ResourceBundle()
        js = { "msg" : messages.get_text(user.account.lang, 'not_enough_funds')}
        return Response(json.dumps(js),  mimetype='application/json', status=400)