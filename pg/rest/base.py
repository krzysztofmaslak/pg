from functools import wraps
from flask import session
import flask

__author__ = 'root'

def authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return flask.make_response('', 401)
        return f(*args, **kwargs)
    return decorated_function