
import json
from pg.rest import base

__author__ = 'xxx'

from flask import Blueprint, jsonify, Response
from flask import request, session

order = Blueprint('order', __name__, url_prefix='/rest/order')

@order.route('/')
@base.authenticated
def list():
    order.logger.debug('['+request.remote_addr+'] list orders username %s, page=%s'%(session['username'], request.args.get('page')))
    user = order.ioc.new_user_service().find_by_username(session['username'])
    orders = order.ioc.new_order_service().find_by_page(user.account, int(request.args.get('page')))
    order.logger.debug('['+request.remote_addr+'] returning %s orders'%(len(orders)))
    count = order.ioc.new_order_service().find_paid_orders_count(user.account)
    js = { "orders" : [o.as_json() for o in orders], "count" : count}
    return Response(json.dumps(js),  mimetype='application/json')
