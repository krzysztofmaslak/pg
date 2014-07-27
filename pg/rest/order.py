
__author__ = 'xxx'

import json
from pg.rest import base
from pg.util.http_utils import get_customer_ip
from flask import Blueprint, jsonify, Response
from flask import request, session

order_blueprint = Blueprint('order', __name__, url_prefix='/rest/order')

@order_blueprint.route('/refund')
@base.authenticated
def refund():
    order_blueprint.logger.debug('['+get_customer_ip()+'] process order refund request by username %s, order_id=%s'%(session['username'], request.args.get('id')))
    user = order_blueprint.ioc.new_user_service().find_by_username(session['username'])
    order = order_blueprint.ioc.new_order_service().find_by_id(int(request.args.get('id')))
    if order.account_id==user.account_id:
        order.ioc.new_order_service().refund_order(order)
        return Response(status=200, mimetype='application/json')
    else:
        return Response(status=400, mimetype='application/json')

@order_blueprint.route('/')
@base.authenticated
def list():
    order_blueprint.logger.debug('['+get_customer_ip()+'] list orders username %s, page=%s'%(session['username'], request.args.get('page')))
    user = order_blueprint.ioc.new_user_service().find_by_username(session['username'])
    orders = order_blueprint.ioc.new_order_service().find_by_page(user.account, int(request.args.get('page')))
    order_blueprint.logger.debug('['+get_customer_ip()+'] returning %s orders'%(len(orders)))
    count = order_blueprint.ioc.new_order_service().find_paid_orders_count(user.account)
    js = { "orders" : [o.as_json() for o in orders], "count" : count}
    return Response(json.dumps(js),  mimetype='application/json')
