
import json
from werkzeug.security import generate_password_hash, check_password_hash
from pg import model, resource_bundle
from pg.util.http_utils import get_customer_ip
from pg.wsgi import detect_language

__author__ = 'xxx'

from flask import Blueprint, Response, session
from flask import request

login_blueprint = Blueprint('login', __name__, url_prefix='/rest/login')

@login_blueprint.route('/', methods=['POST'])
def login():
    username = request.json['username']
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    login_blueprint.logger.info('['+get_customer_ip()+'] Processing authentication request')
    user = login_blueprint.ioc.new_user_service().find_by_username(username)
    if user is not None and user.active:
        if check_password_hash(user.password, request.json['password']):
            login_blueprint.logger.info('['+get_customer_ip()+'] Authentication successful')
            session['username'] = username
            return Response(status=200, mimetype='application/json')
        else:
            error_message = messages.get_text(lang, 'login_wrong_username_or_password')
            login_blueprint.logger.info('['+get_customer_ip()+'] Authentication failed password mismatch')
    else:
        if user is None:
            error_message = messages.get_text(lang, 'login_wrong_username_or_password')
        else:
            error_message = messages.get_text(lang, 'login_user_inactive')
        login_blueprint.logger.info('['+get_customer_ip()+'] Authentication failed no user for username:'+username)
    return Response(json.dumps({"error_message": error_message}),  status=409, mimetype='application/json')