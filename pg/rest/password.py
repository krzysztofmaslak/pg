import hashlib
import uuid

__author__ = 'root'

import json
from werkzeug.security import generate_password_hash, check_password_hash
from pg import model, resource_bundle
from pg.wsgi import detect_language

__author__ = 'xxx'

from flask import Blueprint, Response, session
from flask import request

password_blueprint = Blueprint('password', __name__, url_prefix='/rest/password')

@password_blueprint.route('/reset', methods=['POST'])
def reset():
    password_blueprint.logger.info('['+request.remote_addr+'] Processing reset password request')
    user = password_blueprint.ioc.new_user_service().find_by_username(request.json['username'])
    messages = resource_bundle.ResourceBundle()
    if user is not None:
        user.reset_hash = str(uuid.uuid4())
        model.base.db.session.commit()
        reset_password_subject = resource_bundle.ResourceBundle().get_text(user.account.lang, 'reset_password')
        reset_password_email = model.Email()
        reset_password_email.language = user.account.lang
        reset_password_email.ref_id = user.id
        reset_password_email.type = 'RESET_PASSWORD'
        reset_password_email.from_address = password_blueprint.ioc.get_config()['no_reply']
        reset_password_email.to_address = user.username
        reset_password_email.subject = reset_password_subject
        password_blueprint.ioc.new_email_service().save(reset_password_email)
        success_message = messages.get_text(user.account.lang, 'reset_password_link_info')
        return Response(json.dumps({"success_message": success_message}),  status=200, mimetype='application/json')
    else:
        password_blueprint.logger.info('['+request.remote_addr+'] Failed to request reset password, no such user')
        error_message = messages.get_text(user.account.lang, 'reset_password_no_email')
        return Response(json.dumps({"error_message": error_message}), status=204, mimetype='application/json')

@password_blueprint.route('/new', methods=['POST'])
def new():
    messages = resource_bundle.ResourceBundle()
    password_blueprint.logger.info('['+request.remote_addr+'] Processing new password request')
    password = request.json['password']
    if password==request.json['confirmPassword']:
        reset_hash = request.json['h']
        email_hash = request.json['e']
        user = password_blueprint.ioc.new_user_service().find_by_reset_hash(reset_hash)
        if user is not None:
            if hashlib.sha224(user.username.encode('utf-8')).hexdigest()==email_hash:
                user.password = generate_password_hash(password)
                user.active = True
                model.base.db.session.commit()
                password_blueprint.logger.info('['+request.remote_addr+'] Authenticating after password reset')
                session['username'] = user.username
                return Response(status=200, mimetype='application/json')
            else:
                password_blueprint.logger.info('['+request.remote_addr+'] Failed to process new password request, email hash invalid')
        else:
            password_blueprint.logger.info('['+request.remote_addr+'] Failed to process new password request, no such user')
    else:
        password_blueprint.logger.info('['+request.remote_addr+'] Failed to process new password request, password mismatch confirm password')
        lang = detect_language()
        error_message = messages.get_text(lang, 'new_password_mismatch')
        return Response(json.dumps({"error_message": error_message}), status=400, mimetype='application/json')
