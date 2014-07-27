__author__ = 'root'

from flask import request

def get_customer_ip():
    ip = request.headers.get('X-Real-IP')
    if ( ip is not None):
        ip = request.headers.get('X-Forwarded-For')
        if ip is not None:
            return ip
        else:
            return request.remote_addr