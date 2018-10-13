from pprint import pprint

from flask import Flask
from flask_restplus import Api

from resources.auth_token import AuthTokenFactory
from resources.const import HEADER_AUTH_TOKEN, PRIVATE_KEY, AUTH_FACTORY, MOVIE_DATASET

app = Flask(__name__)
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


def run_from_cmd_line(app):
    import argparse
    parser = argparse.ArgumentParser(description='Run API server.')
    parser.add_argument(PRIVATE_KEY, type=str, help="Path to private key.")
    parser.add_argument("--port", "-p", type=int, default=5001)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--dataset", choices=("full", "small"), default="full")
    args = parser.parse_args()
    # print(args)
    app.config[MOVIE_DATASET] = args.dataset
    path_to_private_key = getattr(args, PRIVATE_KEY)
    app.config[AUTH_FACTORY] = AuthTokenFactory.withPrivateKeyFile(
        path_to_private_key=path_to_private_key
    )
    # pprint(app.config)
    app.run(debug=args.debug, port=args.port)


if __name__ == '__main__':
    run_from_cmd_line(app=app)
