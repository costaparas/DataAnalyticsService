# appropriated from here: https://github.com/mysilver/COMP9321-Data-Services/blob/master/Week8_Authentication/activity_3.py
from time import time

from itsdangerous import (
    JSONWebSignatureSerializer,
    SignatureExpired,
)


# https://en.wikipedia.org/wiki/JSON_Web_Token
# iat: Issued at Time
# exp: Expiration time

class AuthTokenFactory:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate(self, lifetime_in_seconds=300, **kwargs):
        info = {
            'exp': time() + lifetime_in_seconds
        }
        if 'exp' in kwargs:
            raise Exception("'exp' is a reserved key value.")
        info.update(**kwargs)
        token = self.serializer.dumps(info)
        return token.decode()

    def validate(self, token):
        info = self.serializer.loads(token.encode())
        if time() > info['exp']:
            raise SignatureExpired("Token has expired, get a new token.")
        return info




