import os

from tokens import AuthTokenFactory, DEFAULT_TOKEN_LIFETIME


def cmd_generate_token(args):
    path_private_key = os.path.abspath(args.private_key)
    print("Using private key: {}".format(path_private_key))
    auth_factory = AuthTokenFactory.withPrivateKeyFile(path_private_key)
    token = auth_factory.generate(lifetime_in_seconds=args.token_lifetime)
    print("Generating token with lifespan of {} seconds.".format(args.token_lifetime))
    if args.output is not None:
        output_path = os.path.abspath(args.output)
        if os.path.exists(output_path):
            raise Exception("File {} already exists.".format(output_path))
        else:
            print("Writing token to: {}".format(output_path))
            with open(args.output, "w") as f:
                f.write(token)
    else:
        print("Not writing token to disk.")

    print("")
    print(token)


def cmd_line():
    import argparse
    parser = argparse.ArgumentParser(description='Generate API tokens.')
    parser.add_argument("private_key", type=str, help="Path to private key.")
    parser.add_argument("--output", "-o", type=str, default=None, help="Write generated token to file.")
    parser.add_argument("--token_lifetime", type=int, default=DEFAULT_TOKEN_LIFETIME,
                        help="Token lifetime in seconds. Default is 30 days.")

    args = parser.parse_args()
    print(args)
    # key = open(args.private_key,encoding="utf8").read()
    # auth_factory = AuthTokenFactory(private_key=key)
    cmd_generate_token(args)


if __name__ == '__main__':
    cmd_line()
