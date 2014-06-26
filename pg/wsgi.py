from functools import wraps
import os
import traceback
import sys
import errno
from werkzeug.utils import secure_filename
from wtforms import Form, TextField, PasswordField
from werkzeug.security import check_password_hash
from pg import resource_bundle

__author__ = 'xxx'


from flask import Blueprint, session, redirect, request, g, Response
from flask import render_template
from wand.image import Image
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

@wsgi_blueprint.route('/x/<offer_code>', methods=['GET'])
def show_offer(offer_code):
    resource_bundle = resource_bundle.ResourceBundle()
    # todo calculate customer language
    lang = 'eng'
    wsgi_blueprint.logger.info('['+request.remote_addr+'] loading offer page by hash: %s'%offer_code)
    return render_template('offer.html',
                           messages=resource_bundle.get_all(lang),
                           language = lang,
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

@wsgi_blueprint.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        wsgi_blueprint.logger.info('['+request.remote_addr+'] Processing authentication request')
        user = wsgi_blueprint.ioc.new_user_service().find_by_username(form.username.data)
        if user is not None:
            if check_password_hash(user.password, form.password.data):
                wsgi_blueprint.logger.info('['+request.remote_addr+'] Authentication successful')
                session['username'] = form.username.data
                return redirect('/admin/')
            else:
                wsgi_blueprint.logger.info('['+request.remote_addr+'] Authentication failed password mismatch')
        else:
            wsgi_blueprint.logger.info('['+request.remote_addr+'] Authentication failed no user for username:'+form.username.data)
    return render_template('login.html', form=form, project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'])

@wsgi_blueprint.route('/admin/')
@login_required
def admin_landing():
    return render_template('admin/landing.html', project_version=wsgi_blueprint.ioc.get_config()['PROJECT_VERSION'])
