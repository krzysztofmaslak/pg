from collections import namedtuple
import glob
import json
import os
from pg import model, util, wsgi
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
@wsgi.catch_exceptions
def list():
    offer.logger.debug('['+get_customer_ip()+'] list offers username %s, page=%s'%(session['username'], request.args.get('page')))
    user = offer.ioc.new_user_service().find_by_username(session['username'])
    offers = offer.ioc.new_offer_service().find_by_page(user.account, int(request.args.get('page')))
    offer.logger.debug('['+get_customer_ip()+'] returning %s offers'%(len(offers)))
    count = offer.ioc.new_offer_service().find_offers_count(user.account)
    js = { "offers" : [o.as_json() for o in offers], "count" : count}
    return Response(json.dumps(js),  mimetype='application/json')

@offer.route('/account/<hash>', methods=['GET'])
@wsgi.catch_exceptions
def get_by_account(hash):
    offer.logger.debug('['+get_customer_ip()+'] retrieve offers by hash %s'%hash)
    account = offer.ioc.new_account_service().find_by_hash(hash)
    offers = offer.ioc.new_offer_service().find_by_account_id(account.id)
    js = {"offers" : [o.as_json() for o in offers]}
    return Response(json.dumps(js),  mimetype='application/json')

@offer.route('/<hash>', methods=['GET'])
@wsgi.catch_exceptions
def get_by_hash(hash):
    offer.logger.debug('['+get_customer_ip()+'] retrieve offer by hash %s'%hash)
    js = offer.ioc.new_offer_service().find_by_hash(hash).as_json()
    return Response(json.dumps(js),  mimetype='application/json')

@offer.route('/description/<hash>/<id>', methods=['GET'])
@wsgi.catch_exceptions
def get_offer_description_by_hash(hash, id):
    o = offer.ioc.new_offer_service().find_by_hash(hash)
    lang = request.args.get('lang')
    project_version=offer.ioc.get_config()['PROJECT_VERSION']
    html = '<html><head><link href="/static/'+str(project_version)+'/css/style.css" rel="stylesheet" media="screen" /></head><body>'
    if o.items is not None and o.items.count()>0:
        for item in o.items.all():
            if str(item.id)==str(id):
                item = o.items[0]
                if item.img is not None:
                    html += "<img src='/static/images/"+item.img+"_500.png' style='float:left;margin:30px;margin-left:10px;margin-top:10px;margin-bottom:10px;width:200px;'/>"
                html += util.LocaleUtil().get_localized_description(item, lang)
    html = html+'</html>'
    return Response(html,  mimetype='text/html')

@offer.route('/new', methods=['POST'])
@base.authenticated
@wsgi.catch_exceptions
def new_offer():
    user = offer.ioc.new_user_service().find_by_username(session['username'])
    o = offer.ioc.new_offer_service().new_offer(user.account)
    return jsonify({'id':o.id})

@offer_item.route('/new', methods=['POST'])
@base.authenticated
@wsgi.catch_exceptions
def new_offer_item():
    user = offer_item.ioc.new_user_service().find_by_username(session['username'])
    oi = offer_item.ioc.new_offer_service().new_offer_item(user.account, request.json['offer_id'])
    return jsonify({'id':oi.id})

@offer_item_variation.route('/new', methods=['POST'])
@base.authenticated
@wsgi.catch_exceptions
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
@wsgi.catch_exceptions
def save():
    user = offer.ioc.new_user_service().find_by_username(session['username'])
    offer.logger.debug('['+get_customer_ip()+'] save offer %s'%json.dumps(request.json))
    x = json.loads(json.dumps(request.json), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    o = offer.ioc.new_offer_service().save_offer(user.account, x)
    return Response(json.dumps(o.as_json()),  mimetype='application/json')

@offer.route('/<offer_id>', methods=['DELETE'])
@base.authenticated
@wsgi.catch_exceptions
def delete(offer_id):
    user = offer.ioc.new_user_service().find_by_username(session['username'])
    offer.ioc.new_offer_service().delete_offer(user.account, offer_id)
    return Response(status=200)

@offer.route('/image/<target>/<id>', methods=['DELETE'])
@base.authenticated
@wsgi.catch_exceptions
def delete_image(target, id):
    user = offer.ioc.new_user_service().find_by_username(session['username'])
    if target=='additional_image':
        offer.logger.debug('['+get_customer_ip()+'] delete additional image id:'+id)
        image = offer.ioc.new_image_service().find_by_id(int(id))
        if image.offer_item.offer.account_id==user.account_id:
            for fl in glob.glob(offer.ioc.get_config()['UPLOAD_FOLDER']+'/'+target+'/'+id+'*'):
                os.remove(fl)
            offer.ioc.new_image_service().delete(image)
            return Response(status=200)
    elif target=='offer_item':
        offer.logger.debug('['+get_customer_ip()+'] delete image - target offer_item')
        offer_item = offer.ioc.new_offer_service().find_offer_item_by_id(id)
        if offer_item.offer.account_id==user.account_id:
            offer_item.img=None
            for fl in glob.glob(offer.ioc.get_config()['UPLOAD_FOLDER']+'/'+target+'/'+id+'*'):
                os.remove(fl)
            if offer_item.variations.count()>0:
                for variation in offer_item.variations:
                    if variation.img is None and variation.img is not None:
                        offer_item.img = variation.img
            model.base.db.session.commit()
            return Response(status=200)
    else:
        offer_item_variation = offer.ioc.new_offer_service().find_offer_item_variation_by_id(id)
        if offer_item_variation.offer_item.offer.account_id==user.account_id:
            offer_item_variation.img=None
            for fl in glob.glob(offer.ioc.get_config()['UPLOAD_FOLDER']+'/'+target+'/'+id+'*'):
                os.remove(fl)
            offer.logger.debug('['+get_customer_ip()+'] deleted images')
            model.base.db.session.commit()
            return Response(status=200)
    return Response(status=400)
