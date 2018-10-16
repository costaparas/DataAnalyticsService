from flask import Flask
from flask_restplus import Api

from resources.auth_token import AuthTokenFactory
from resources.const import HEADER_AUTH_TOKEN, PRIVATE_KEY, AUTH_FACTORY, MOVIE_DATASET

from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

api = Api(app,
          title="Movie Recommendation API",
          description="This API provides access to a database of movie titles and movie recommendations.",
          version="1.0",
          authorizations={
              'apiKey': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': HEADER_AUTH_TOKEN
              }
          },
          security="apiKey"
          )
api.namespaces.clear()

from resources.movie import api as movie_api
from resources.recommendation import api as recom_api
from resources.auth_endpoint import api as token_api

api.add_namespace(movie_api)
api.add_namespace(recom_api)
api.add_namespace(token_api)


def parse_cmd_line_args():
    import argparse
    parser = argparse.ArgumentParser(description='Run API server.')
    parser.add_argument(PRIVATE_KEY, type=str, help="Path to private key.", nargs='?')
    parser.add_argument("--port", "-p", type=int, default=5001)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--dataset", choices=("full", "small"), default="full")
    args = parser.parse_args()
    return args


def run_from_cmd_line(app):
    import sys, os
    args = parse_cmd_line_args()
    app.config[MOVIE_DATASET] = args.dataset

    # use environment variable if no private key file supplied
    # this approach is used in the deployed api
    path_to_private_key = '.private-key'
    if 'PRIVATE_KEY' in os.environ:
        with open('.private-key', 'w') as f:
            f.write(os.environ['PRIVATE_KEY'])
    else:
        path_to_private_key = getattr(args, PRIVATE_KEY)
        if not path_to_private_key:
            print('%s: missing private key' %sys.argv[0], file=sys.stderr)
            sys.exit(1)

    app.config[AUTH_FACTORY] = AuthTokenFactory.withPrivateKeyFile(
        path_to_private_key=path_to_private_key
    )

    # override port number with environment variable
    # this approach is used in the deployed api
    port = args.port
    if 'PORT' in os.environ:
        port = os.environ['PORT']

    app.run(debug=args.debug, port=port, host='0.0.0.0')


if __name__ == '__main__':
    run_from_cmd_line(app=app)
