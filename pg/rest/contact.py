from collections import namedtuple
import json
from pg.rest import base
from pg.util.http_utils import get_customer_ip
from pg.wsgi import detect_language

__author__ = 'xxx'

from flask import Blueprint, jsonify, Response
from flask import request, session
from pg import model, resource_bundle, wsgi

contact_blueprint = Blueprint('contact', __name__, url_prefix='/rest/contact')

@contact_blueprint.route('/', methods=['POST'])
@wsgi.catch_exceptions
def new_message():
    contact_blueprint.logger.info('['+get_customer_ip()+'] Send contact message')
    oi = contact_blueprint.ioc.new_contact_service().save_conctact(model.Contact(get_customer_ip(), request.json['email'], request.json['message']))
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    admin_email = model.Email()
    admin_email.type = 'ADMIN_CONTACT_EMAIL'
    admin_email.ref_id = oi.id
    admin_email.from_address = contact_blueprint.ioc.get_config()['contact_email']
    admin_email.to_address = contact_blueprint.ioc.get_config()['contact_email']
    admin_email.subject = "Cusomer message"
    contact_blueprint.ioc.new_email_service().save(admin_email)

    return jsonify({'id':oi.id, 'success_message':messages.get_text(lang, 'contact_message_success')})
