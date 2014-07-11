from functools import wraps
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

__author__ = 'xxx'


from flask import Blueprint, session, redirect, request, g, Response
from flask import render_template
from wand.image import Image
from pg import model
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

@wsgi_blueprint.route('/x/<offer_code>', methods=['GET'])
def show_offer(offer_code):
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    wsgi_blueprint.logger.info('['+request.remote_addr+'] loading offer page by hash: %s'%offer_code)
    offer = wsgi_blueprint.ioc.new_offer_service().find_by_hash(offer_code)
    return render_template('offer.html',
                           messages=messages.get_all(lang),
                           language = lang,
                           title=offer.title,
                           countries = [c.as_json() for c in wsgi_blueprint.ioc.new_country_service().find_all()],
                           project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
                           stripe_publishable=wsgi_blueprint.ioc.get_config()['stripe.publishable'])

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

@wsgi_blueprint.route('/api/image/<target>/<id>', methods=['POST'])
def upload_image(target, id):
    wsgi_blueprint.logger.info('['+request.remote_addr+'] Starting image upload')
    try:
        file = request.files['file']
        wsgi_blueprint.logger.info('['+request.remote_addr+'] Starting image upload file=%s'%file.filename)
        if file and allowed_file(file.filename):
            wsgi_blueprint.logger.debug('['+request.remote_addr+'] image extenssion allowed')
            filename = secure_filename(file.filename)
            mkdirs(wsgi_blueprint.ioc.get_config()['UPLOAD_FOLDER']+'/'+target)
            file.save(wsgi_blueprint.ioc.get_config()['UPLOAD_FOLDER']+'/'+target+'/'+id+'.png')
            try:
                with Image(filename=wsgi_blueprint.ioc.get_config()['UPLOAD_FOLDER']+'/'+target+'/'+id+'.png') as img:
                    with img.clone() as i:
                        i.resize(int(100), int(100/i.width*i.height))
                        i.save(filename=wsgi_blueprint.ioc.get_config()['UPLOAD_FOLDER']+'/'+target+'/'+id+'_thumb.png')
                return Response(status=200)
            except IOError:
                traceback.print_exc(file=sys.stdout)
                print("cannot create thumbnail for '%s'" % filename)
                return Response(status=500)
        else:
            wsgi_blueprint.logger.debug('['+request.remote_addr+'] extenssion not allowed filename=%s'%file.filename)
            return Response(status=400)
    except:
        traceback.print_exc(file=sys.stdout)
        return Response(status=400)


@wsgi_blueprint.route('/')
def index():
    return render_template('index.html')


class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')

class RegisterForm(Form):
    username = EmailField('Username')
    password = PasswordField('Password')

class ResetPassword(Form):
    username = TextField('Username')

@wsgi_blueprint.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error_message = None
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    if request.method == 'POST' and form.validate():
        wsgi_blueprint.logger.info('['+request.remote_addr+'] Processing authentication request')
        user = wsgi_blueprint.ioc.new_user_service().find_by_username(form.username.data)
        if user is not None and user.active:
            if check_password_hash(user.password, form.password.data):
                wsgi_blueprint.logger.info('['+request.remote_addr+'] Authentication successful')
                session['username'] = form.username.data
                return redirect('/admin/')
            else:
                error_message = messages.get_text(lang, 'login_wrong_username_or_password')
                wsgi_blueprint.logger.info('['+request.remote_addr+'] Authentication failed password mismatch')
        else:
            if user is None:
                error_message = messages.get_text(lang, 'login_wrong_username_or_password')
            else:
                error_message = messages.get_text(lang, 'login_user_inactive')
            wsgi_blueprint.logger.info('['+request.remote_addr+'] Authentication failed no user for username:'+form.username.data)

    return render_template('login.html', form=form,
                           project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
                           message_login=messages.get_text(lang, 'login_title'),
                           message_remin_me_my_password=messages.get_text(lang, 'login_remind_me_my_password'),
                           message_username=messages.get_text(lang, 'login_username'),
                           message_username_placeholder=messages.get_text(lang, 'login_username_placeholder'),
                           message_password=messages.get_text(lang, 'login_password'),
                           message_password_placeholder=messages.get_text(lang, 'login_password_placeholder'),
                           message_login_btn=messages.get_text(lang, 'login_btn'),
                           error_message=error_message)

@wsgi_blueprint.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    error_message = None
    success_message = None
    messages = resource_bundle.ResourceBundle()
    lang = detect_language()
    if request.method == 'POST' and form.validate():
        wsgi_blueprint.logger.info('['+request.remote_addr+'] Processing registration request')
        user = wsgi_blueprint.ioc.new_user_service().find_by_username(form.username.data)
        if user is None:
            a = model.Account()
            a.properties.append(model.Property(a, 'sales.email', form.username.data))
            a.lang = detect_language()
            u = model.User(form.username.data, generate_password_hash(form.password.data))
            a.users.append(u)
            wsgi_blueprint.ioc.new_account_service().save(a)
            success_message = messages.get_text(lang, 'register_success')

            registration_email = wsgi_blueprint.ioc.get_config()['registration_email']
            customer_email = model.Email()
            customer_email.type = "REGISTRATION"
            customer_email.from_address = registration_email
            customer_email.to_address = u.username
            customer_email.language = lang
            messages = resource_bundle.ResourceBundle()
            customer_email.subject = messages.get_text(lang, 'registration_email_subject')
            wsgi_blueprint.ioc.new_email_service().save(customer_email)

            admin_email = model.Email()
            admin_email.type = 'REGISTRATION_ADMIN'
            admin_email.from_address = registration_email
            admin_email.to_address = registration_email
            admin_email.subject = "New customer: "+u.username
            wsgi_blueprint.ioc.new_email_service().save(admin_email)
            model.base.db.session.commit()
        else:
            wsgi_blueprint.logger.info('['+request.remote_addr+'] Registration failed, user already exist')
            error_message = messages.get_text(lang, 'register_user_already_exist')
    return render_template('register.html', form=form,
                           project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
                           message_register=messages.get_text(lang, 'register_title'),
                           message_username=messages.get_text(lang, 'register_username'),
                           message_username_placeholder=messages.get_text(lang, 'register_username_placeholder'),
                           message_password=messages.get_text(lang, 'register_password'),
                           message_password_placeholder=messages.get_text(lang, 'register_password_placeholder'),
                           message_register_btn=messages.get_text(lang, 'register_btn'),
                           error_message=error_message,
                           success_message=success_message
    )

@wsgi_blueprint.route('/reset_password.html', methods=['GET', 'POST'])
def reset_password():
    form = RegisterForm(request.form)
    messages = resource_bundle.ResourceBundle()
    success_message = None
    lang = detect_language()
    if request.method == 'POST' and form.validate():
        wsgi_blueprint.logger.info('['+request.remote_addr+'] Processing reset password request')
        user = wsgi_blueprint.ioc.new_user_service().find_by_username(form.username.data)
        if user is not None:
            user.reset_hash = str(uuid.uuid4())
            model.base.db.session.commit()
            ps = wsgi_blueprint.ioc.new_property_service()
            reset_password_subject = resource_bundle.ResourceBundle().get_text(user.account.lang, 'reset_password')
            reset_password_email = model.Email()
            reset_password_email.ref_id = user.id
            reset_password_email.type = 'RESET_PASSWORD'
            reset_password_email.from_address = ps.find_value_by_code(user.account, 'sales.email')
            reset_password_email.to_address = user.username
            reset_password_email.subject = reset_password_subject
            wsgi_blueprint.ioc.new_email_service().save(reset_password_email)
            success_message = messages.get_text(lang, 'reset_password_link_info')
        else:
            wsgi_blueprint.logger.info('['+request.remote_addr+'] Failed to request reset password, no such user')
    return render_template('reset_password.html', form=form,
                           project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'],
                           message_reset_password = messages.get_text(lang, 'reset_password_title'),
                           message_username = messages.get_text(lang, 'reset_password_username'),
                           message_username_placeholder = messages.get_text(lang, 'reset_password_placeholder'),
                           message_reset_password_btn = messages.get_text(lang, 'reset_password_btn'),
                           success_message=success_message
    )

@wsgi_blueprint.route('/admin/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect("/index.html")

@wsgi_blueprint.route('/admin/')
@login_required
def admin_landing():
    messages = resource_bundle.ResourceBundle()
    user = wsgi_blueprint.ioc.new_user_service().find_by_username(session['username'])
    admin_title = messages.get_text(user.account.lang, 'admin_title')
    return render_template('admin/landing.html',
                           balance = user.account.balance,
                           admin_title = admin_title,
                           messages=messages.get_all(user.account.lang),
                           countries = [c.as_json() for c in wsgi_blueprint.ioc.new_country_service().find_all()],
                           project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'])
