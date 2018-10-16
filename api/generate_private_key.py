import os
import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 required.")
else:
    import secrets

NUM_BYTES = 128


def generate_key():
    return secrets.token_urlsafe(NUM_BYTES)


def cmd_line():
    import argparse
    parser = argparse.ArgumentParser(description='Generate private key')
    parser.add_argument("output", type=str)
    args = parser.parse_args()
    if os.path.exists(args.output):
        raise Exception("File {} already exists.".format(args.output))
    else:
        key = generate_key()
        print(key)
        with open(os.open(args.output, os.O_CREAT | os.O_WRONLY, 0o600), "w") as f:
            f.write(key)


if __name__ == '__main__':
    cmd_line()
