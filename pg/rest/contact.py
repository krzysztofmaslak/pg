from collections import namedtuple
import json
from pg.rest import base
from pg.wsgi import detect_language

__author__ = 'xxx'

from flask import Blueprint, jsonify, Response
from flask import request, session
from pg import model, resource_bundle

contact_blueprint = Blueprint('contact', __name__, url_prefix='/rest/contact')

@contact_blueprint.route('/', methods=['POST'])
def new_message():
    contact_blueprint.logger.info('['+request.remote_addr+'] Send contact message')
    oi = contact_blueprint.ioc.new_contact_service().save_conctact(model.Contact(request.remote_addr, request.json['email'], request.json['message']))
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    admin_email = model.Email()
    admin_email.type = 'ADMIN_CONTACT_EMAIL'
    admin_email.ref_id = oi.id
    admin_email.from_address = register_rest.ioc.get_config()['contact_email']
    admin_email.to_address = register_rest.ioc.get_config()['contact_email']
    admin_email.subject = "Cusomer message"
    contact_blueprint.ioc.new_email_service().save(admin_email)

    return jsonify({'id':oi.id, 'success_message':messages.get_text(lang, 'contact_message_success')})
