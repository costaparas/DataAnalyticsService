from functools import wraps

from flask import request, current_app
from flask_restplus import abort
from itsdangerous import BadSignature, SignatureExpired

from .const import HEADER_AUTH_TOKEN, AUTH_FACTORY


def requires_auth(api):
    def decorator(f):
        @wraps(f)
        @api.response(401, "Unauthenticated.")
        def decorated(*args, **kwargs):
            token = request.headers.get(HEADER_AUTH_TOKEN)
            if not token:
                abort(401, 'Authentication token is missing')
            else:
                auth = current_app.config.get(AUTH_FACTORY)
                try:
                    token_payload = auth.validate(token)
                    return f(*args, **kwargs)
                except BadSignature:
                    abort(401, "Invalid token")
                except SignatureExpired:
                    abort(401, "Expired token")

        return decorated

    return decorator