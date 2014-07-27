__author__ = 'root'

from flask import request

def get_customer_ip():
    ip = request.headers.get('X-Real-IP')
    if ( ip is not None):
        return ip
    else:
        ip = request.headers.get('X-Forwarded-For')
        if ip is not None:
            return ip
        else:
            ip = request.remote_addr
            if ip is not None:
                return ip
            else:
                return ''