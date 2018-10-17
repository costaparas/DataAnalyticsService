from functools import wraps

from flask import request, current_app
from flask_restplus import abort
from itsdangerous import BadSignature, SignatureExpired

from .const import HEADER_AUTH_TOKEN, AUTH_FACTORY
from .app_context import get_auth

def requires_auth(api):
    def decorator(f):
        @wraps(f)
        @api.response(401, "Unauthenticated.")
        def decorated(*args, **kwargs):
            token = request.headers.get(HEADER_AUTH_TOKEN)
            if not token:
                abort(401, 'Authentication token is missing.')
            else:
                try:
                    auth = get_auth()
                    if auth is not None:
                        token_payload = get_auth().validate(token)
                    return f(*args, **kwargs)
                except BadSignature:
                    abort(401, "Invalid token")
                except SignatureExpired:
                    abort(401, "Expired token")

        return decorated

    return decorator