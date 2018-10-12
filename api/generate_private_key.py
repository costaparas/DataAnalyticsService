import sys
import os
import secrets
import base64
NUM_BYTES = 128

def generate_key():
    if sys.version_info[0] < 3:
        return base64.b64encode(os.urandom(NUM_BYTES))
    else:
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
        with open(args.output, "w") as f:
            f.write(key)


if __name__ == '__main__':
    cmd_line()
