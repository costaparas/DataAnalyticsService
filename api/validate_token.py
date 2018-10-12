import os
from datetime import datetime

from ago import human
from itsdangerous import SignatureExpired, BadSignature

from token import AuthTokenFactory
from pprint import pprint


def cmd_validate_token(args, verbose=False):
    path_private_key = os.path.abspath(args.private_key)
    auth_factory = AuthTokenFactory.withPrivateKeyFile(path_private_key)
    path_token = os.path.abspath(args.token_file)
    token = open(path_token, encoding="utf8").read()
    if verbose:
        print("Using private key: {}".format(path_private_key))
        print("Validating token: {}".format(path_token))
    try:
        token_payload = auth_factory.validate(token=token)
        print("Token is valid.")
        delta = datetime.now() - datetime.fromtimestamp(token_payload['exp'])
        print("Expires", human(delta, precision=2))
        if verbose:
            print("Token payload:")
            pprint(token_payload)


    except SignatureExpired as e:
        print("Token expired")

    except BadSignature as e:
        print("Token invalid")


def cmd_line():
    import argparse
    parser = argparse.ArgumentParser(description='Validate API tokens.')
    parser.add_argument("private_key", type=str, help="Path to private key.")
    parser.add_argument("token_file", type=str, help="Path to token to validate.")
    parser.add_argument('-v', '--verbose', action='count', default=0)

    args = parser.parse_args()
    # print(args)
    cmd_validate_token(args, verbose=(args.verbose>0))


if __name__ == '__main__':
    cmd_line()
