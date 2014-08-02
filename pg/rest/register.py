
import json
import uuid
from werkzeug.security import generate_password_hash
from pg import model, resource_bundle
from pg.util.http_utils import get_customer_ip
from pg.wsgi import detect_language

__author__ = 'xxx'

from flask import Blueprint, Response, session
from flask import request

register_rest = Blueprint('register', __name__, url_prefix='/rest/register')

@register_rest.route('/', methods=['POST'])
def register():
    account_name = request.json['name']
    account = register_rest.ioc.new_account_service().find_by_name(account_name)
    lang = detect_language()
    messages = resource_bundle.ResourceBundle()
    if account is None:
        username = request.json['username']
        register_rest.logger.info('['+get_customer_ip()+'] Processing registration request')
        user = register_rest.ioc.new_user_service().find_by_username(username)
        if user is None:
            a = model.Account()
            a.name = account_name
            a.lang = detect_language()
            u = model.User(username, generate_password_hash(request.json['password']))
            u.activation_hash = str(uuid.uuid4())
            a.users.append(u)
            register_rest.ioc.new_account_service().save(a)
            success_message = messages.get_text(lang, 'register_success')

            registration_email = register_rest.ioc.get_config()['registration_email']
            customer_email = model.Email()
            customer_email.type = "REGISTRATION"
            customer_email.from_address = registration_email
            customer_email.ref_id = u.id
            customer_email.to_address = u.username
            customer_email.language = lang
            messages = resource_bundle.ResourceBundle()
            customer_email.subject = messages.get_text(lang, 'registration_email_subject')
            register_rest.ioc.new_email_service().save(customer_email)

            admin_email = model.Email()
            admin_email.type = 'REGISTRATION_ADMIN'
            admin_email.from_address = registration_email
            admin_email.to_address = registration_email
            admin_email.subject = "New customer: "+u.username
            register_rest.ioc.new_email_service().save(admin_email)

            if register_rest.ioc.get_config()['SKIP_ACCOUNT_ACTIVATION']:
                u.active = True
                session['username'] = u.username
            model.base.db.session.commit()
            register_rest.logger.info('['+get_customer_ip()+'] Registration successful')

            return Response(json.dumps({"success_message": success_message, 'skip_activation':register_rest.ioc.get_config()['SKIP_ACCOUNT_ACTIVATION']}),  status=200, mimetype='application/json')
        else:
            register_rest.logger.info('['+get_customer_ip()+'] Registration failed, user already exist')
            error_message = messages.get_text(lang, 'register_user_already_exist')
            return Response(json.dumps({"error_message": error_message}),  status=409, mimetype='application/json')
    else:
        register_rest.logger.info('['+get_customer_ip()+'] Registration failed, account already exist')
        error_message = messages.get_text(lang, 'register_account_already_exist')
        return Response(json.dumps({"error_message": error_message}),  status=409, mimetype='application/json')
