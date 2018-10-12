# appropriated from here: https://github.com/mysilver/COMP9321-Data-Services/blob/master/Week8_Authentication/activity_3.py
from time import time

from itsdangerous import (
    JSONWebSignatureSerializer,
    SignatureExpired,
)
import os

SECONDS_IN_A_DAY = 60 * 60 * 24
SECONDS_IN_30_DAYS = 30 * SECONDS_IN_A_DAY
DEFAULT_TOKEN_LIFETIME = SECONDS_IN_30_DAYS

class AuthTokenFactory:
    @staticmethod
    def withPrivateKeyFile(path_to_private_key):
        key = open(path_to_private_key,encoding="utf8").read()
        auth_factory = AuthTokenFactory(private_key=key)
        return auth_factory

    def __init__(self, private_key):
        self.private_key = private_key
        self.serializer = JSONWebSignatureSerializer(private_key)

    def generate(self, lifetime_in_seconds=DEFAULT_TOKEN_LIFETIME, **kwargs):
        # exp: Expiration time
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





if __name__ == '__main__':
    pass
