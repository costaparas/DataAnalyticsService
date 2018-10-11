#appropriated from here: https://github.com/mysilver/COMP9321-Data-Services/blob/master/Week8_Authentication/activity_3.py
from time import time
from itsdangerous import (
    JSONWebSignatureSerializer,
    SignatureExpired,
    BadSignature,
)
# https://en.wikipedia.org/wiki/JSON_Web_Token
# iat: Issued at Time
# exp: Expiration time

class AuthenticationToken:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate(self, lifetime_in_seconds=300, **kwargs):
        info = {
            'exp' : time() + lifetime_in_seconds
        }
        info.update(**kwargs)

        token = self.serializer.dumps(info)
        return token.decode()

    def validate(self, token):
        info = self.serializer.loads(token.encode())
        token_age = time() - info['creation_time']
        if token_age > self.expires_in:
            raise SignatureExpired("The Token has been expired; get a new token")

        return info['username']

def test_auth_tokens():
    SECRET_KEY = "ahslkjdf234ulwken"
    auth = AuthenticationToken(secret_key=SECRET_KEY, )