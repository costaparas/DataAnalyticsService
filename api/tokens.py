# appropriated from here: https://github.com/mysilver/COMP9321-Data-Services/blob/master/Week8_Authentication/activity_3.py
from time import time

from itsdangerous import (
    JSONWebSignatureSerializer,
    SignatureExpired,
)
import os

class AuthTokenFactory:
    def __init__(self, private_key):
        self.private_key = private_key
        self.serializer = JSONWebSignatureSerializer(private_key)

    def generate(self, lifetime_in_seconds=300, **kwargs):
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


SECONDS_IN_A_DAY = 60 * 60 * 24
SECONDS_IN_30_DAYS = 30 * SECONDS_IN_A_DAY


def cmd_line():
    import argparse
    parser = argparse.ArgumentParser(description='Generate and validate API tokens.')
    parser.add_argument("action", choices=("generate", "validate"))
    parser.add_argument("private_key", type=str, help="Path to private key.")
    parser.add_argument("--output","-o", type=str, default=None, help="Write generated token to file.")
    parser.add_argument("--token_lifetime", type=int, default=SECONDS_IN_30_DAYS, help="Token lifetime in seconds. Default is 30 days.")

    args = parser.parse_args()
    print(args)
    key = open(args.private_key,encoding="utf8").read()
    auth_factory = AuthTokenFactory(private_key=key)
    if args.action == "generate":
        token = auth_factory.generate(lifetime_in_seconds=args.token_lifetime)
        print("Generating token with lifespan of {} seconds.".format(args.token_lifetime))
        print(token)
        if args.output is not None:
            if os.path.exists(args.output):
                raise Exception("File {} already exists.".format(args.output))
            else:
                with open(args.output, "w") as f:
                    f.write(token)

    elif args.action == "validate":
        pass


if __name__ == '__main__':
    cmd_line()
    # pass
