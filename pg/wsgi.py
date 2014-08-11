from argparse import _ActionsContainer
from functools import wraps
import hashlib
import os
import traceback
import sys
import errno
import uuid
from werkzeug.utils import secure_filename
from wtforms import Form, TextField, PasswordField
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms.fields.html5 import EmailField
from pg import resource_bundle
from pg.util.http_utils import get_customer_ip

__author__ = 'xxx'


from flask import Blueprint, session, redirect, request, g, Response
from flask import render_template
from wand.image import Image
from pg import model, util
import locale
import re
wsgi_blueprint = Blueprint('wsgi', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login.html')
        user_service = wsgi_blueprint.ioc.new_user_service()
        user = user_service.find_by_username(session['username'])

        if user is None:
            return redirect('/login.html')
        return f(*args, **kwargs)
    return decorated_function

def catch_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            wsgi_blueprint.logger.exception(e)
            return render_template('500.html',
               project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
            )
    return decorated_function

LANGUAGE_CODES = ('en')

# From django.utils.translation.trans_real.parse_accept_lang_header
accept_language_re = re.compile(r'''
    ([A-Za-z]{1,8}(?:-[A-Za-z]{1,8})*|\*) # "en", "en-au", "x-y-z", "*"
    (?:\s*;\s*q=(0(?:\.\d{,3})?|1(?:.0{,3})?))? # Optional "q=1.00", "q=0.8"
    (?:\s*,\s*|$) # Multiple accepts per header.
    ''', re.VERBOSE)

def parse_accept_lang_header(lang_string):
    """
    Parses the lang_string, which is the body of an HTTP Accept-Language
    header, and returns a list of (lang, q-value), ordered by 'q' values.

    Any format errors in lang_string results in an empty list being returned.
    """
    result = []
    pieces = accept_language_re.split(lang_string)
    if pieces[-1]:
        return []
    for i in range(0, len(pieces) - 1, 3):
        first, lang, priority = pieces[i : i + 3]
        if first:
            return []
        priority = priority and float(priority) or 1.0
        result.append((lang, priority))
    result.sort(key=lambda k: k[1], reverse=True)
    return result

# From django.utils.translation.trans_real.to_locale
def to_locale(language, to_lower=False):
    """
    Turns a language name (en-us) into a locale name (en_US). If 'to_lower' is
    True, the last component is lower-cased (en_us).
    """
    p = language.find('-')
    if p >= 0:
        if to_lower:
            return language[:p].lower()+'_'+language[p+1:].lower()
        else:
            # Get correct locale for sr-latn
            if len(language[p+1:]) > 2:
                return language[:p].lower()+'_'+language[p+1].upper()+language[p+2:].lower()
            return language[:p].lower()+'_'+language[p+1:].upper()
    else:
        return language.lower()

def parse_http_accept_language(accept):
    for accept_lang, unused in parse_accept_lang_header(accept):
        if accept_lang == '*':
            break

        # We have a very restricted form for our language files (no encoding
        # specifier, since they all must be UTF-8 and only one possible
        # language each time. So we avoid the overhead of gettext.find() and
        # work out the MO file manually.

        # 'normalized' is the root name of the locale in POSIX format (which is
        # the format used for the directories holding the MO files).
        normalized = locale.locale_alias.get(to_locale(accept_lang, True))
        if not normalized:
            continue
        # Remove the default encoding from locale_alias.
        normalized = normalized.split('.')[0]

        for lang_code in (accept_lang, accept_lang.split('-')[0]):
            lang_code = lang_code.lower()
            if lang_code in LANGUAGE_CODES:
                return lang_code
    return None

def detect_language():
    if request.args.get('lang') is not None:
        return request.args.get('lang')
    else:
        lang = parse_http_accept_language(request.headers.get('Accept-Language', ''))
        if lang is None:
            return 'en'
        else:
            return lang

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def get_sha_part(hash):
    return hash[len('pbkdf2:sha1:'):]

@wsgi_blueprint.route('/', methods=['GET', 'POST'])
@wsgi_blueprint.route('/index.html', methods=['GET', 'POST'])
@catch_exceptions
def index():
    return redirect('/register.html')

@wsgi_blueprint.route('/api/image/<offer_item_id>/<target>/<id>', methods=['POST'])
@catch_exceptions
def upload_image(offer_item_id, target, id):
    wsgi_blueprint.logger.info('['+get_customer_ip()+'] Starting image upload')
    try:
        file = request.files['file']
        wsgi_blueprint.logger.info('['+get_customer_ip()+'] Starting image upload file=%s'%file.filename)
        if file and allowed_file(file.filename):
            wsgi_blueprint.logger.debug('['+get_customer_ip()+'] image extenssion allowed')
            filename = secure_filename(file.filename)
            mkdirs(wsgi_blueprint.ioc.get_config()['UPLOAD_FOLDER']+'/'+target)
            file.save(wsgi_blueprint.ioc.get_config()['UPLOAD_FOLDER']+'/'+target+'/'+id+'.png')
            offer_item = wsgi_blueprint.ioc.new_offer_service().find_offer_item_by_id(offer_item_id)
            user = wsgi_blueprint.ioc.new_user_service().find_by_username(session['username'])
            if offer_item.offer.account_id!=user.account_id:
                raise RuntimeError('Tried to change image for different account') 
            if target=='offer_item':
                offer_item.img = target+'/'+id
            elif offer_item.img is not None and offer_item.img.startswith('offer_item_variation'):
                offer_item.img = target+'/'+id
            if target.startswith('offer_item_variation'):
                offer_item_variation = wsgi_blueprint.ioc.new_offer_service().find_offer_item_variation_by_id(id)
                offer_item_variation.img = target+'/'+id
            model.base.db.session.commit()
            try:
                with Image(filename=wsgi_blueprint.ioc.get_config()['UPLOAD_FOLDER']+'/'+target+'/'+id+'.png') as img:
                    with img.clone() as i:
                        i.resize(int(100), int(100/i.width*i.height))
                        i.save(filename=wsgi_blueprint.ioc.get_config()['UPLOAD_FOLDER']+'/'+target+'/'+id+'_thumb.png')
                    with img.clone() as i:
                        i.compression_quality=99
                        i.resize(int(500), int(500/i.width*i.height))
                        i.save(filename=wsgi_blueprint.ioc.get_config()['UPLOAD_FOLDER']+'/'+target+'/'+id+'_500.png')
                return Response(status=200)
            except IOError:
                traceback.print_exc(file=sys.stdout)
                print("cannot create thumbnail for '%s'" % filename)
                return Response(status=500)
        else:
            wsgi_blueprint.logger.debug('['+get_customer_ip()+'] extenssion not allowed filename=%s'%file.filename)
            return Response(status=400)
    except:
        traceback.print_exc(file=sys.stdout)
        return Response(status=400)

@wsgi_blueprint.route('/login.html', methods=['GET'])
@catch_exceptions
def login():
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    activation_hash = request.args.get('h')
    email_hash = request.args.get('e')
    if activation_hash is not None and email_hash is not None:
        wsgi_blueprint.logger.info('['+get_customer_ip()+'] Starting user activation with h=%s,e=%s'%(activation_hash, email_hash))
        user = wsgi_blueprint.ioc.new_user_service().find_by_activation_hash(activation_hash)
        if user is not None:
            if hashlib.sha224(user.username.encode('utf-8')).hexdigest()==email_hash:
                user.active = True
                model.base.db.session.commit()
                session['username'] = user.username
                return redirect('/admin/')
            else:
                wsgi_blueprint.logger.info('['+get_customer_ip()+'] Failed activation, email hash not equal was: %s, expected: %s'%(hashlib.sha224(user.username.encode('utf-8')).hexdigest(), email_hash))
                # todo handle when hash not equal
        else:
            # todo handle when user is null
            wsgi_blueprint.logger.info('['+get_customer_ip()+'] Failed activation, no user for given hash:%s'%activation_hash)
            pass
    messages = messages.get_all(lang)
    return render_template('main.html',
       project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
       messages=messages,
       page='login'
    )

@wsgi_blueprint.route('/register.html', methods=['GET'])
@catch_exceptions
def register():
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    wsgi_blueprint.logger.info('['+get_customer_ip()+'] Detected customer language %s'%(lang))
    return render_template('main.html',
       project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
       messages=messages.get_all(lang),
       page='register'
    )


@wsgi_blueprint.route('/new-password.html', methods=['GET'])
@catch_exceptions
def new_password():
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    return render_template('main.html',
       project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
       messages=messages.get_all(lang),
       page='new-password'
    )


@wsgi_blueprint.route('/reset-password.html', methods=['GET'])
@catch_exceptions
def reset_password():
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    return render_template('main.html',
       project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
       messages=messages.get_all(lang),
       page='reset-password'
    )

@wsgi_blueprint.route('/contact.html', methods=['GET'])
@catch_exceptions
def contact_form():
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    return render_template('main.html',
       project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
       messages=messages.get_all(lang),
       page='contact'
    )

@wsgi_blueprint.route('/admin/logout')
@catch_exceptions
def do_logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect("/logout.html")

@wsgi_blueprint.route('/logout.html')
@catch_exceptions
def logout():
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    return render_template('main.html',
       project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
       messages=messages.get_all(lang),
       page='logout'
    )

@wsgi_blueprint.route('/privacy-policy.html')
@catch_exceptions
def privacy_policy():
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    return render_template('privacy-policy.html',
       project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
       messages=messages.get_all(lang)
    )

@wsgi_blueprint.route('/admin/')
@login_required
@catch_exceptions
def admin_landing():
    messages = resource_bundle.ResourceBundle()
    user = wsgi_blueprint.ioc.new_user_service().find_by_username(session['username'])
    admin_title = messages.get_text(user.account.lang, 'admin_title')
    return render_template('admin/landing.html',
                           balance = user.account.balance,
                           admin_title = admin_title,
                           admin_lang = user.account.lang,
                           messages=messages.get_all(user.account.lang),
                           countries = [c.as_json() for c in wsgi_blueprint.ioc.new_country_service().find_all()],
                           project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'])

@wsgi_blueprint.route('/<path:path>', methods=['GET'])
@catch_exceptions
def fallback(path):
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    if path.startswith('X'):
    	offer = wsgi_blueprint.ioc.new_offer_service().find_by_hash(path)
    	if offer is not None:
                wsgi_blueprint.logger.info('['+get_customer_ip()+'] loading offer page by hash: %s'%path)
                wsgi_blueprint.ioc.new_event_service().persist(model.Event(get_customer_ip(), offer.account, path))
                offer_title = util.LocaleUtil().get_localized_title(offer, lang)
                return render_template('offer.html',
			        messages=messages.get_all(lang),
               		language = lang,
               		title=offer_title,
               		account_hash = offer.account.hash,
               		account_name = offer.account.name.replace("'", "&#39;"),
               		countries = [c.as_json() for c in wsgi_blueprint.ioc.new_country_service().find_all()],
               		project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
               		stripe_publishable=wsgi_blueprint.ioc.get_config()['stripe.publishable'])
    elif path.startswith('S'):
        wsgi_blueprint.logger.info('['+get_customer_ip()+'] loading seller page by hash: %s'%path)	
        account = wsgi_blueprint.ioc.new_account_service().find_by_hash(path)
        if account is not None:
               return render_template('offer_list.html',
                        messages=messages.get_all(lang),
                        language = lang,
                        title=account.name,
                        account_hash = account.hash,
                        account_name = account.name.replace("'", "&#39;"),
			project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'])
        else:
                wsgi_blueprint.logger.info('['+get_customer_ip()+'] could not find seller by name: [%s]'%path)
                return Response(status=404)
    else:
        return Response(status=404)
