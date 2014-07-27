
__author__ = 'xxx'

import json
from pg.rest import base
from pg.util.http_utils import get_customer_ip
from flask import Blueprint, jsonify, Response
from flask import request, session

event_blueprint = Blueprint('event', __name__, url_prefix='/rest/event')

@event_blueprint.route('/')
@base.authenticated
def list():
    user = event_blueprint.ioc.new_user_service().find_by_username(session['username'])
    offer_traffic = event_blueprint.ioc.new_event_service().find_offer_traffic_for(user.account_id, request.args.get('from'), request.args.get('to'))
    return Response(json.dumps(offer_traffic),  mimetype='application/json')
