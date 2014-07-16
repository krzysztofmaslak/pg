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
    return jsonify({'id':oi.id, 'success_message':messages.get_text(lang, 'contact_message_success')})
