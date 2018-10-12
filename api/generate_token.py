import os

from token import AuthTokenFactory, DEFAULT_TOKEN_LIFETIME
from datetime import datetime, timedelta
from ago import human

def cmd_generate_token(args, verbose=False):
    path_private_key = os.path.abspath(args.private_key)
    auth_factory = AuthTokenFactory.withPrivateKeyFile(path_private_key)
    token = auth_factory.generate(lifetime_in_seconds=args.lifetime)
    if verbose:
        print("Using private key: {}".format(path_private_key))
        print("Generating token with lifetime of {human} ({secs} seconds).".format(
            secs=args.lifetime,
            human=human(timedelta(seconds=args.lifetime), past_tense="{0}")

        ))
    if args.output is not None:
        output_path = os.path.abspath(args.output)
        if os.path.exists(output_path):
            raise Exception("File {} already exists.".format(output_path))
        else:
            with open(args.output, "w") as f:
                f.write(token)
            print("Token written to: {}".format(output_path))
    else:
        if verbose:
            print("Not writing token to disk.")
        print(token)



def cmd_line():
    import argparse
    parser = argparse.ArgumentParser(description='Generate API tokens.')
    parser.add_argument("private_key", type=str, help="Path to private key.")
    parser.add_argument("--output", "-o", type=str, default=None, help="Write generated token to file.")
    parser.add_argument("--lifetime", "-l", type=int, default=DEFAULT_TOKEN_LIFETIME,
                        help="Token lifetime in seconds. Default is 30 days.")
    parser.add_argument('-v', '--verbose', action='count', default=0)

    args = parser.parse_args()
    # print(args)
    cmd_generate_token(args, verbose=(args.verbose > 0))


if __name__ == '__main__':
    cmd_line()
