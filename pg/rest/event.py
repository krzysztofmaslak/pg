
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
    events = event_blueprint.ioc.new_event_service().find_by_page(user.account, request.args.get('date'), int(request.args.get('page')))
    events_count = event_blueprint.ioc.new_event_service().find_events_count(user.account, request.args.get('date'))
    js = { "events" : [o.as_json() for o in events], "count" : events_count}
    return Response(json.dumps(js),  mimetype='application/json')
