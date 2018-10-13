from flask import current_app

from .const import AUTH_FACTORY


def get_auth():
    auth = current_app.config.get(AUTH_FACTORY)
    return auth
