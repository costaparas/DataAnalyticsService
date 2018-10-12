import os
from tokens import AuthTokenFactory
from itsdangerous import SignatureExpired, BadSignature
def cmd_validate_token(args):
    path_private_key = os.path.abspath(args.private_key)
    print("Using private key: {}".format(path_private_key))
    auth_factory = AuthTokenFactory.withPrivateKeyFile(path_private_key)
    path_token = os.path.abspath(args.token_file)
    print("Validating token: {}".format(path_token))
    token = open(path_token, encoding="utf8").read()
    try:
        token_payload = auth_factory.validate(token=token)
        print("Token valid.\nPayload:")
        print(token_payload)
    except SignatureExpired as e:
        print("Token expired")

    except BadSignature as e:
        print("Token invalid")
def cmd_line():
    import argparse
    parser = argparse.ArgumentParser(description='Validate API tokens.')
    parser.add_argument("private_key", type=str, help="Path to private key.")
    parser.add_argument("token_file", type=str, help="Path to token to validate.")

    args = parser.parse_args()
    print(args)
    cmd_validate_token(args)


if __name__ == '__main__':
    cmd_line()
