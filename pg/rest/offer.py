from collections import namedtuple
import json
from pg.rest import base
from pg.util.http_utils import get_customer_ip

__author__ = 'xxx'

from flask import Blueprint, jsonify, Response
from flask import request, session

offer = Blueprint('offer', __name__, url_prefix='/rest/offer')
offer_item = Blueprint('offer_item', __name__, url_prefix='/rest/offer_item')
offer_item_variation = Blueprint('offer_item_variation', __name__, url_prefix='/rest/offer_item_variation')

@offer.route('/')
@base.authenticated
def list():
    offer.logger.debug('['+get_customer_ip()+'] list offers username %s, page=%s'%(session['username'], request.args.get('page')))
    user = offer.ioc.new_user_service().find_by_username(session['username'])
    offers = offer.ioc.new_offer_service().find_by_page(user.account, int(request.args.get('page')))
    offer.logger.debug('['+get_customer_ip()+'] returning %s offers'%(len(offers)))
    count = offer.ioc.new_offer_service().find_offers_count(user.account)
    js = { "offers" : [o.as_json() for o in offers], "count" : count}
    return Response(json.dumps(js),  mimetype='application/json')

@offer.route('/<hash>', methods=['GET'])
def get_by_hash(hash):
    offer.logger.debug('['+get_customer_ip()+'] retrieve offer by hash %s'%hash)
    js = offer.ioc.new_offer_service().find_by_hash(hash).as_json()
    return Response(json.dumps(js),  mimetype='application/json')

@offer.route('/new', methods=['POST'])
@base.authenticated
def new_offer():
    user = offer.ioc.new_user_service().find_by_username(session['username'])
    o = offer.ioc.new_offer_service().new_offer(user.account)
    return jsonify({'id':o.id})

@offer_item.route('/new', methods=['POST'])
@base.authenticated
def new_offer_item():
    user = offer_item.ioc.new_user_service().find_by_username(session['username'])
    oi = offer_item.ioc.new_offer_service().new_offer_item(user.account, request.json['offer_id'])
    return jsonify({'id':oi.id})

@offer_item_variation.route('/new', methods=['POST'])
@base.authenticated
def new_offer_item_variation():
    user = offer_item_variation.ioc.new_user_service().find_by_username(session['username'])
    count = int(request.json['count'])
    if count>3:
        count = 3
    ids = []
    for index in range(count):
        item = offer_item_variation.ioc.new_offer_service().new_offer_item_variation(user.account, request.json['offer_item_id'])
        ids.append(item.id)
    return Response(json.dumps(ids),  mimetype='application/json')

@offer.route('/', methods=['POST'])
@base.authenticated
def save():
    user = offer.ioc.new_user_service().find_by_username(session['username'])
    offer.logger.debug('['+get_customer_ip()+'] save offer %s'%json.dumps(request.json))
    x = json.loads(json.dumps(request.json), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    o = offer.ioc.new_offer_service().save_offer(user.account, x)
    return Response(json.dumps(o.as_json()),  mimetype='application/json')

@offer.route('/<offer_id>', methods=['DELETE'])
@base.authenticated
def delete(offer_id):
    user = offer.ioc.new_user_service().find_by_username(session['username'])
    offer.ioc.new_offer_service().delete_offer(user.account, offer_id)
    return Response(status=200)